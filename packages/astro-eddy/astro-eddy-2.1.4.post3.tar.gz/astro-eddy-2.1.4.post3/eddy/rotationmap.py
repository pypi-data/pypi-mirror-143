# -*- coding: utf-8 -*-

import time
import zeus
import emcee
import numpy as np
import scipy.constants as sc
from .datacube import datacube
from .helper_functions import plot_walkers, plot_corner, random_p0
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")


class rotationmap(datacube):
    """
    Read in the velocity maps and initialize the class. To make the fitting
    quicker, we can clip the cube to a smaller region, or downsample the
    image to get a quicker initial fit.

    Args:
        path (str): Relative path to the rotation map you want to fit.
        FOV (Optional[float]): If specified, clip the data down to a
            square field of view with sides of `FOV` [arcsec].
        uncertainty (Optional[str]): Relative path to the map of v0
            uncertainties. Must be a FITS file with the same shape as the
            data. If nothing is specified, will tried to find an uncerainty
            file following the ``bettermoments`` format. If this is not found,
            it will assume a 10% on all pixels.
        downsample (Optional[int]): Downsample the image by this factor for
            quicker fitting. For example, using ``downsample=4`` on an image
            which is 1000 x 1000 pixels will reduce it to 250 x 250 pixels.
            If you use ``downsample='beam'`` it will sample roughly
            spatially independent pixels using the beam major axis as the
            spacing.
    """

    priors = {}
    SHO_priors = {}

    def __init__(self, path, FOV=None, uncertainty=None, downsample=None):
        datacube.__init__(self, path=path, FOV=FOV, fill=None)
        if self.header['bunit'].lower() not in ['m/s', 'km/s']:
            msg = "What is the velocity unit? Either `m/s` or `km/s`."
            self.velocity_unit = input(msg)
        else:
            self.velocity_unit = self.header['bunit'].lower()
        self.data *= 1e3 if self.velocity_unit == 'km/s' else 1.0
        self.mask = np.isfinite(self.data)
        self._readuncertainty(uncertainty=uncertainty, FOV=FOV)
        if downsample is not None:
            self.downsample_cube(downsample)
        self.vlsr = np.nanmedian(self.data)
        self.vlsr_kms = self.vlsr / 1e3
        self._set_default_priors()

    # -- FITTING FUNCTIONS -- #

    def fit_map(self, p0, params, r_min=None, r_max=None, optimize=True,
                nwalkers=None, nburnin=300, nsteps=100, scatter=1e-3,
                plots=None, returns=None, pool=None, mcmc='emcee',
                mcmc_kwargs=None, niter=1):
        """
        Fit a rotation profile to the data. Note that for a disk with
        a non-zero height, the sign of the inclination dictates the direction
        of rotation: a positive inclination denotes a clockwise rotation, while
        a negative inclination denotes an anti-clockwise rotation.

        The function must be provided with a dictionary of parameters,
        ``params`` where key is the parameter and its value is either the fixed
        value this will take,

            ``params['PA'] = 45.0``

        would fix position angle to 45 degrees. Or, if an integeter, the index
        in the starting positions, ``p0``, such that,

            ``params['mstar'] = 0``

        would mean that the first value in ``p0`` is the guess for ``'mstar'``.

        For a list of the geometrical parameters, included flared emission
        surfaces or warps, see :func:`disk_coords`. In addition to these
        geometrical properties ``params`` also requires ``'mstar'``,
        ``'vlsr'``, ``'dist'``.

        To include a spatial convolution of the model rotation map you may also
        set ``params['beam']=True``, however this is only really necessary for
        low spatial resolution data, or for rotation maps made via the
        intensity-weighted average velocity.

        .. _Rosenfeld et al. (2013): https://ui.adsabs.harvard.edu/abs/2013ApJ...774...16R/abstract

        Args:
            p0 (list): List of the free parameters to fit.
            params (dictionary): Dictionary of the model parameters.
            r_min (optional[float]): Inner radius to fit in [arcsec].
            r_max (optional[float]): Outer radius to fit in [arcsec].
            optimize (optional[bool]): Use ``scipy.optimize`` to find the
                ``p0`` values which maximize the likelihood. Better results
                will likely be found. Note that for the masking the default
                ``p0`` and ``params`` values are used for the deprojection, or
                those foundvfrom the optimization. If this results in a poor
                initial mask, try with ``optimise=False`` or with a ``niter``
                value larger than 1.
            nwalkers (optional[int]): Number of walkers to use for the MCMC.
            nburnin (optional[int]): Number of steps to discard for burn-in.
            nsteps (optional[int]): Number of steps to use to sample the
                posterior distributions.
            scatter (optional[float]): Scatter used in distributing walker
                starting positions around the initial ``p0`` values.
            plots (optional[list]): List of the diagnostic plots to make. This
                can include ``'mask'``, ``'walkers'``, ``'corner'``,
                ``'bestfit'``, ``'residual'``, or ``'none'`` if no plots are to
                be plotted. By default, all are plotted.
            returns (optional[list]): List of items to return. Can contain
                ``'samples'``, ``'sampler'``, ``'percentiles'``, ``'dict'``,
                ``'model'``, ``'residuals'`` or ``'none'``. By default only
                ``'percentiles'`` are returned.
            pool (optional): An object with a `map` method.
            mcmc_kwargs (Optional[dict]): Dictionary to pass to the MCMC
                ``EnsembleSampler``.
            niter (optional[int]): Number of iterations to perform using the
                median PDF values from the previous MCMC run as starting
                positions. This is probably only useful if you have no idea
                about the starting positions for the emission surface or if you
                want to remove walkers stuck in local minima.

        Returns:
            to_return (list): Depending on the returns list provided.
                ``'samples'`` will be all the samples of the posteriors (with
                the burn-in periods removed). ``'percentiles'`` will return the
                16th, 50th and 84th percentiles of each posterior functions.
                ``'dict'`` will return a dictionary of the median parameters
                which can be directly input to other functions.
        """

        # Check the dictionary. May need some more work.

        if r_min is not None:
            if 'r_min' in params.keys():
                print("Found `r_min` in `params`. Overwriting value.")
            params['r_min'] = r_min
        if r_max is not None:
            if 'r_max' in params.keys():
                print("Found `r_max` in `params`. Overwriting value.")
            params['r_max'] = r_max

        params_tmp = self.verify_params_dictionary(params.copy())

        # Generate the mask for fitting based on the params.

        p0 = np.squeeze(p0).astype(float)
        temp = rotationmap._populate_dictionary(p0, params_tmp)
        self.ivar = self._calc_ivar(temp)

        # Check what the parameters are.

        labels = rotationmap._get_labels(params_tmp)
        labels_raw = []
        for label in labels:
            label_raw = label.replace('$', '').replace('{', '')
            label_raw = label_raw.replace(r'\rm ', '').replace('}', '')
            labels_raw += [label_raw]
        if len(labels) != len(p0):
            raise ValueError("Mismatch in labels and p0. Check for integers.")
        print("Assuming:\n\tp0 = [%s]." % (', '.join(labels_raw)))

        # Run an initial optimization using scipy.minimize. Recalculate the
        # inverse variance mask.

        if optimize:
            p0 = self._optimize_p0(p0, params_tmp)

        # Set up and run the MCMC with emcee.

        time.sleep(0.5)
        nsteps = np.atleast_1d(nsteps)
        nburnin = np.atleast_1d(nburnin)
        nwalkers = np.atleast_1d(nwalkers)

        mcmc_kwargs = {} if mcmc_kwargs is None else mcmc_kwargs
        mcmc_kwargs['scatter'], mcmc_kwargs['pool'] = scatter, pool

        for n in range(int(niter)):

            # Make the mask for fitting.

            temp = rotationmap._populate_dictionary(p0, params_tmp)
            temp = self.verify_params_dictionary(temp)
            self.ivar = self._calc_ivar(temp)

            # Run the sampler.

            sampler = self._run_mcmc(p0=p0, params=params_tmp,
                                     nwalkers=nwalkers[n % nwalkers.size],
                                     nburnin=nburnin[n % nburnin.size],
                                     nsteps=nsteps[n % nsteps.size],
                                     mcmc=mcmc, **mcmc_kwargs)

            if type(params_tmp['PA']) is int:
                sampler.chain[:, :, params_tmp['PA']] %= 360.0

            # Split off the samples.

            samples = sampler.get_chain(discard=nburnin[-1], flat=True)
            p0 = np.median(samples, axis=0)
            medians = rotationmap._populate_dictionary(p0, params.copy())
            medians = self.verify_params_dictionary(medians)

        # Diagnostic plots.

        if plots is None:
            plots = ['walkers', 'corner', 'bestfit', 'residual']
        plots = np.atleast_1d(plots)
        if 'none' in plots:
            plots = []
        if 'walkers' in plots:
            if mcmc == 'emcee':
                walkers = sampler.chain.T
            else:
                walkers = np.rollaxis(sampler.chain.copy(), 2)
            plot_walkers(walkers, nburnin[-1], labels)
        if 'corner' in plots:
            plot_corner(samples, labels)
        if 'bestfit' in plots:
            self.plot_model(samples=samples,
                            params=params,
                            mask=self.ivar,
                            draws=10)
        if 'residual' in plots:
            self.plot_model_residual(samples=samples,
                                     params=params,
                                     mask=self.ivar,
                                     draws=10)

        # Generate the output.

        to_return = []

        if returns is None:
            returns = ['samples']
        returns = np.atleast_1d(returns)

        if 'none' in returns:
            return None
        if 'samples' in returns:
            to_return += [samples]
        if 'sampler' in returns:
            to_return += [sampler]
        if 'lnprob' in returns:
            to_return += [sampler.lnprobability[nburnin:]]
        if 'percentiles' in returns:
            to_return += [np.percentile(samples, [16, 50, 84], axis=0)]
        if 'dict' in returns:
            to_return += [medians]
        if 'model' in returns or 'residual' in returns:
            model = self.evaluate_models(samples, params)
            if 'model' in returns:
                to_return += [model]
            if 'residual' in returns:
                to_return += [self.data * 1e3 - model]

        return to_return if len(to_return) > 1 else to_return[0]

    def fit_annuli(self, rpnts=None, rbins=None, x0=0.0, y0=0.0, inc=0.0,
                   PA=0.0, z0=0.0, psi=1.0, r_cavity=None, r_taper=None,
                   q_taper=None, w_i=None, w_r=None, w_t=None, z_func=None,
                   shadowed=False, phi_min=None, phi_max=None,
                   exclude_phi=False, abs_phi=False, mask_frame='disk',
                   user_mask=None, fit_vrot=True, fit_vrad=True,
                   fix_vlsr=False, plots=None, returns=None,
                   optimize_kwargs=None, MCMC=False):
        r"""
        Splits the map into concentric annuli based on the geometrical
        parameters, then fits each annnulus with a simple harmonic oscillator
        model,

        .. math::

            v(\phi) = v_{\phi} \cos(\rm \phi) \pm v_{\rm rad} \sin(\phi) + v_{\rm lsr}

        where the :math:`\pm` arises due to the projection of the radial
        velocity, defined such that positive values are away from the star,
        along the line of sight.

        .. note::
            If you find negative :math:`v_{\phi}` values then your chosen
            position angle is likely off by 180 degrees.

        Args:
            rpnts
            rbins
            x0 (Optional[float]): Source right ascension offset [arcsec].
            y0 (Optional[float]): Source declination offset [arcsec].
            inc (Optional[float]): Source inclination [degrees]. A positive
                inclination denotes a disk rotating clockwise on the sky, while
                a negative inclination represents a counter-clockwise rotation.
            PA (Optional[float]): Source position angle [degrees]. Measured
                between north and the red-shifted semi-major axis in an
                easterly direction.
            z0 (Optional[float]): Aspect ratio at 1" for the emission surface.
                To get the far side of the disk, make this number negative.
            psi (Optional[float]): Flaring angle for the emission surface.
            z1 (Optional[float]): Correction term for ``z0``.
            phi (Optional[float]): Flaring angle correction term for the
                emission surface.
            r_cavity (Optional[float]): Outer radius of a cavity. Within this
                region the emission surface is taken to be zero.
            w_i (Optional[float]): Warp inclination in [degrees] at the disk
                center.
            w_r (Optional[float]): Scale radius of the warp in [arcsec].
            w_t (Optional[float]): Angle of nodes of the warp in [degrees].
            z_func (Optional[callable]): A user-defined emission surface
                function that will return ``z`` in [arcsec] for a given ``r``
                in [arcsec]. This will override the analytical form.
            shadowed (Optional[bool]): Whether to use the slower, but more
                robust method for deprojecting pixel values.
            phi_min (Optional[float]): Minimum polar angle of the segment of
                the annulus in [degrees]. Note this is the polar angle, not the
                position angle.
            phi_max (Optional[float]): Maximum polar angle of the segment of
                the annulus in [degrees]. Note this is the polar angle, not the
                position angle.
            exclude_phi (Optional[bool]): If ``True``, exclude the provided
                polar angle range rather than include it.
            abs_phi (Optional[bool]): If ``True``, take the absolute value of
                the polar angle such that it runs from 0 [deg] to 180 [deg].
            mask_frame (Optional[str]): Which frame the radial and azimuthal
                mask is specified in, either ``'disk'`` or ``'sky'``.
            user_mask (Optional[ndarray]): A 2D mask to use.
            fit_vrot (Optional[bool]): Whether to include rotational velocities
                in the fit. Default is ``True``.
            fit_vrad (Optional[bool]): Whether to include radial velocities in
                    the fit. Default is ``True``.
            fix_vlsr (Optional[bool/float]): Fix the systemic velocity to this
                value in the fitting, otherwise allow it to be a free
                parameter. Default is ``False``.
            plots (Optional[list]): Plots to generate after the fitting. Can be
                either of ``'model'`` and ``'residual'``. Default is both.
            returns (Optional[list]): List of objects to return. Can be any of
                ``'profiles'``, ``'model'`` or ``'residual'``.
            optimize_kwargs (Optional[dict]): Kwargs to pass to
                ``scipy.optimize.curve_fit``.

        Returns:
            Depends on the value of ``returns``.
        """

        # Get the radial binning and deprojected radius and phi values.

        rpnts, rbins = self._get_radial_bins(rpnts=rpnts, rbins=rbins)
        rvals, pvals = self.disk_coords(x0=x0, y0=y0, inc=inc, PA=PA, z0=z0,
                                        psi=psi, r_cavity=r_cavity,
                                        r_taper=r_taper, q_taper=q_taper,
                                        w_i=w_i, w_r=w_r, w_t=w_t,
                                        z_func=z_func, shadowed=shadowed)[:2]

        # Cycle through each annulus to include the fit.

        fits, uncertainty = [], []
        nparams = 2 + int(fit_vrad) - int(bool(fix_vlsr))
        for r_min, r_max in zip(rbins[:-1], rbins[1:]):

            # Define the annulus mask. If there are no pixels in it, continue
            # to the next annulus.

            try:
                mask = self.get_mask(r_min=r_min, r_max=r_max, phi_min=phi_min,
                                     phi_max=phi_max, exclude_phi=exclude_phi,
                                     abs_phi=abs_phi, x0=x0, y0=y0, inc=inc,
                                     PA=PA, z0=z0, psi=psi, r_cavity=r_cavity,
                                     r_taper=r_taper, q_taper=q_taper, w_i=w_i,
                                     w_r=w_r, w_t=w_t, z_func=z_func,
                                     shadowed=shadowed, mask_frame=mask_frame,
                                     user_mask=user_mask)
            except ValueError:
                popt = np.ones(nparams) * np.nan
                fits += [popt]
                uncertainty += [popt]
                continue

            # Extract the finite pixels.

            x = pvals.copy()[mask].flatten()
            y = self.data.copy()[mask].flatten()
            dy = self.error.copy()[mask].flatten()
            isfinite = np.isfinite(y) & np.isfinite(dy)
            x, y, dy = x[isfinite], y[isfinite], dy[isfinite]

            # Fit the pixels, and correct the radial velocity to have positive
            # velocities describining motions away from the star.

            try:
                popt, cvar = self._fit_SHO(x=x, y=y, dy=dy,
                                           fit_vrot=fit_vrot,
                                           fit_vrad=fit_vrad,
                                           fix_vlsr=fix_vlsr,
                                           MCMC=MCMC,
                                           optimize_kwargs=optimize_kwargs)
            except ValueError:
                popt = np.ones(nparams) * np.nan
                fits += [popt]
                uncertainty += [popt]
                continue

            if fit_vrad and inc >= 0.0:
                if fit_vrot:
                    popt[1] *= -1.0
                else:
                    popt[0] *= -1.0

            fits += [popt]
            uncertainty += [cvar]

        # Transform the arrays so they're in the shape (nparam, nrad).

        fits = np.atleast_2d(fits).T
        uncertainty = np.atleast_2d(uncertainty).T

        # Build the linearly interpolated model.

        model = self._evaluate_annuli_model(rpnts=rpnts, fits=fits,
                                            rvals=rvals, pvals=pvals,
                                            fit_vrot=fit_vrot,
                                            fit_vrad=fit_vrad,
                                            fix_vlsr=fix_vlsr)

        # Make the plots.

        plots = ['profiles', 'model', 'residual'] if plots is None else plots
        plots = np.atleast_1d(plots)
        if 'profiles' in plots:
            self.plot_velocity_profiles(rpnts=rpnts,
                                        fits=fits,
                                        uncertainty=uncertainty,
                                        fit_vrot=fit_vrot,
                                        fit_vrad=fit_vrad,
                                        fix_vlsr=fix_vlsr)
        if 'model' in plots:
            self.plot_model(model=model)
        if 'residual' in plots:
            self.plot_model_residual(model=model)

        # Generate the retuns.

        returns = ['profiles'] if returns is None else np.atleast_1d(returns)
        returns = np.atleast_1d(returns)
        to_return = []
        if 'profiles' in returns:
            to_return += [rpnts, fits, uncertainty]
        if 'model' in returns:
            to_return += [model]
        if 'residual' in returns:
            to_return += [self.data - model]
        return to_return

    def _evaluate_annuli_model(self, rpnts, fits, rvals, pvals, fit_vrot=True,
                               fit_vrad=True, fix_vlsr=False):
        """
        Evaluate the annuli models onto a 2D map. Fits must not be deprojected.

        Args:
            rpnts (array): A size M array of radial positions.
            fits (array): A [NxM] array containing the inferred velocity
                values where N is the number of velocity components (1, 2, 3).
            rvals (array): A 2D array of on-sky radial positions in [arcsec].
            pvals (array): A 2D array of on-sky polar angle in [radians].
            fit_vrot (Optional[bool]): If v_rot is included in ``fits``.
            fit_vrad (Optional[bool]): If v_rad is included in ``fits``.
            fix_vlsr (Optional[bool/float]): If ``False``, v_z is included in
                ``fits``, otherwise this specifies the fized ``vlsr``.

        Returns:
            v0
        """
        from scipy.interpolate import interp1d
        idx = 0
        if fit_vrot:
            vrot = interp1d(rpnts, fits[idx], bounds_error=False)(rvals)
            idx += 1
        else:
            vrot = 0.0
        if fit_vrad:
            vrad = interp1d(rpnts, fits[idx], bounds_error=False)(rvals)
            idx += 1
        else:
            vrad = 0.0
        if not fix_vlsr:
            vlsr = interp1d(rpnts, fits[idx], bounds_error=False)(rvals)
        else:
            vlsr = fix_vlsr
        return vrot * np.cos(pvals) + vrad * np.sin(pvals) + vlsr

    def _fit_SHO(self, x, y, dy, fit_vrot=True, fit_vrad=True, fix_vlsr=False,
                 optimize_kwargs=None, MCMC=False):
        """Fit the points with a simple harmonic oscillator."""

        from .helper_functions import SHO_double

        # Guess the starting parameters.

        vrot = 0.5 * (y.max() - y.min())
        vrad = 0.0
        vlsr = fix_vlsr if fix_vlsr else y.mean()

        # Define the function to fit the data.

        if not fix_vlsr:
            if fit_vrot and fit_vrad:
                def func(x, *params):
                    return SHO_double(x, *params)
                p0 = [vrot, vrad, vlsr]
                priors = ['vrot', 'vrad', 'vlsr']
            elif fit_vrot and (not fit_vrad):
                def func(x, *params):
                    return SHO_double(x, params[0], 0.0, params[-1])
                p0 = [vrot, vlsr]
                priors = ['vrot', 'vlsr']
            elif (not fit_vrot) and fit_vrad:
                def func(x, *params):
                    return SHO_double(x, 0.0, params[0], params[-1])
                p0 = [vrad, vlsr]
                priors = ['vrad', 'vlsr']
            else:
                def func(x, *params):
                    return SHO_double(x, 0.0, 0.0, *params)
                p0 = [vlsr]
                priors = ['vlsr']
        else:
            if fit_vrot and fit_vrad:
                def func(x, *params):
                    return SHO_double(x, *params, fix_vlsr)
                p0 = [vrot, vrad]
                priors = ['vrot', 'vrad']
            elif fit_vrot and (not fit_vrad):
                def func(x, *params):
                    return SHO_double(x, *params, 0.0, fix_vlsr)
                p0 = [vrot]
                priors = ['vrot']
            elif (not fit_vrot) and fit_vrad:
                def func(x, *params):
                    return SHO_double(x, 0.0, *params, fix_vlsr)
                p0 = [vrad]
                priors = ['vrad']
            else:
                raise ValueError("You must fit one parameter!")

        # Returns if no values are provided.

        if len(y) == 0:
            popt = np.empty(len(p0))
            cvar = popt.copy()
            return popt, cvar

        # Send values to with curve_fit or emcee.

        if MCMC:
            return self._SHO_MCMC(x, y, dy, func, p0, priors, optimize_kwargs)
        else:
            return self._SHO_chi2(x, y, dy, func, p0, optimize_kwargs)

    def _SHO_chi2(self, x, y, dy, func, p0, optimize_kwargs=None):
        """Use scipy.optimize.curve_fit for the fitting."""
        from scipy.optimize import curve_fit

        # Set up the optimization.

        kw = {} if optimize_kwargs is None else optimize_kwargs
        kw['p0'] = p0
        kw['sigma'] = dy
        kw['absolute_sigma'] = True
        kw['maxfev'] = kw.pop('maxfev', 10000)

        # Try the fitting. If it fails, just return NaNs.

        try:
            popt, cvar = curve_fit(func, x, y, **kw)
            cvar = np.diag(cvar)**0.5
        except (ValueError, TypeError):
            popt = np.empty(len(p0))
            cvar = popt.copy()
        return popt, cvar

    def _SHO_MCMC(self, x, y, dy, func, p0, priors, optimize_kwargs=None):
        """Use an MCMC sampler to model the posteriors."""

        # Set up the optimization.

        kw = {} if optimize_kwargs is None else optimize_kwargs
        if kw.pop('mcmc', 'emcee') == 'zeus':
            EnsembleSampler = zeus.EnsembleSampler
        else:
            EnsembleSampler = emcee.EnsembleSampler
        nwalkers = kw.pop('nwalkers', 128)
        nburnin = kw.pop('nburnin', 200)
        nsteps = kw.pop('nsteps', 100)
        scatter = kw.pop('scatter', 1e-3)
        progress = kw.pop('progress', True)
        moves = kw.pop('moves', None)
        pool = kw.pop('pool', None)

        # Check that the starting positions are OK. If not, return NaN.
        # TODO: Check how to handle this in the model making.

        if not np.isfinite(np.sum([rotationmap.SHO_priors[p](t)
                                   for t, p in zip(p0, priors)])):
            return [np.nan for _ in p0], [np.nan for _ in p0]

        # Run the EnsembleSampler

        p0 = random_p0(p0, scatter, nwalkers)
        sampler = EnsembleSampler(nwalkers,
                                  p0.shape[1],
                                  self._SHO_ln_probability,
                                  args=[func, priors, x, y, dy],
                                  moves=moves,
                                  pool=pool)
        sampler.run_mcmc(p0, nburnin + nsteps, progress=progress, **kw)

        # Extract the median and (symmetric) uncertainties.

        samples = sampler.get_chain(discard=nburnin, flat=True)
        samples = np.percentile(samples, [16, 50, 84], axis=0)
        return samples[1], 0.5 * (samples[2] - samples[0])

    def _SHO_ln_probability(self, theta, func, priors, x, y, dy):
        """Log-probablility function."""
        lnp = self._SHO_ln_prior(theta, priors)
        if np.isfinite(lnp):
            return lnp + self._SHO_ln_likelihood(theta, func, x, y, dy)
        return -np.inf

    def _SHO_ln_prior(self, theta, priors):
        """Priors for the MCMC fitting of the annuli."""
        lnp = 0.0
        for t, p in zip(theta, priors):
            lnp += rotationmap.SHO_priors[p](t)
            if not np.isfinite(lnp):
                return lnp
        return lnp

    def _SHO_ln_likelihood(self, theta, func, x, y, dy):
        """Log-likelihood for the MCMC fitting of the annuli."""
        lnx2 = -0.5 * np.sum(np.power((y - func(x, *theta)) / dy, 2))
        return lnx2 if np.isfinite(lnx2) else -np.inf

    def _get_radial_bins(self, rpnts=None, rbins=None):
        """Return default radial bins."""
        if rpnts is None and rbins is None:
            rbins = np.arange(self.bmaj / 2, self.xaxis[0], self.bmaj / 4)
            rpnts = np.mean([rbins[1:], rbins[:-1]], axis=0)
        elif rpnts is None:
            rpnts = np.mean([rbins[1:], rbins[:-1]], axis=0)
        else:
            dr = np.diff(rpnts) / 2.0
            dr = np.insert(dr, -1, dr[-1])
            if not np.all(np.isclose(dr, dr[0])):
                print("WARNING: Non-linear `rpnts` found. Check results!")
            rbins = np.insert(rpnts + dr, 0, rpnts[0] - dr[0])
        return rpnts, rbins

    def set_prior(self, param, args, type='flat'):
        """
        Set the prior for the given parameter. There are two types of priors
        currently usable, ``'flat'`` which requires ``args=[min, max]`` while
        for ``'gaussian'`` you need to specify ``args=[mu, sig]``.

        Args:
            param (str): Name of the parameter.
            args (list): Values to use depending on the type of prior.
            type (optional[str]): Type of prior to use.
        """
        type = type.lower()
        if type not in ['flat', 'gaussian']:
            raise ValueError("type must be 'flat' or 'gaussian'.")
        if type == 'flat':
            def prior(p):
                if not min(args) <= p <= max(args):
                    return -np.inf
                return np.log(1.0 / (max(args) - min(args)))
        else:
            def prior(p):
                return -0.5 * ((args[0] - p) / args[1])**2
        rotationmap.priors[param] = prior

    def set_SHO_prior(self, param, args, type='flat'):
        """
        Set the prior for the given parameter for the SHO fitting. There are
        two types of priors currently usable, ``'flat'`` which requires
        ``args=[min, max]`` while for ``'gaussian'`` you need to specify
        ``args=[mu, sig]``. The three ``params`` which are available are
        ``'vrot'``, ``'vrad'`` and ``'vlsr'``.

        Args:
            param (str): Name of the parameter.
            args (list): Values to use depending on the type of prior.
            type (optional[str]): Type of prior to use.
        """
        type = type.lower()
        if type not in ['flat', 'gaussian']:
            raise ValueError("type must be 'flat' or 'gaussian'.")
        if type == 'flat':
            def prior(p):
                if not min(args) <= p <= max(args):
                    return -np.inf
                return np.log(1.0 / (args[1] - args[0]))
        else:
            def prior(p):
                return -0.5 * ((args[0] - p) / args[1])**2
        rotationmap.SHO_priors[param] = prior

    def plot_data(self, vmin=None, vmax=None, ivar=None, return_fig=False):
        """
        Plot the first moment map. By default will clip the velocity contours
        such that the velocities around the systemic velocity are highlighted.

        Args:
            levels (optional[list]): List of contour levels to use.
            ivar (optional[ndarray]): Inverse variances for each pixel. Will
                draw a solid contour around the regions with finite ``ivar``
                values and fill regions not considered.
            return_fig (optional[bool]): Return the figure.

        Returns:
            fig (Matplotlib figure): If ``return_fig`` is ``True``. Can access
                the axes through ``fig.axes`` for additional plotting.
        """
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()

        vmin = np.nanpercentile(self.data, [2]) if vmin is None else vmin
        vmax = np.nanpercentile(self.data, [98]) if vmax is None else vmax
        vmax = max(abs(vmin - self.vlsr), abs(vmax - self.vlsr))
        im = ax.imshow(self.data / 1e3, origin='lower', extent=self.extent,
                       vmin=(self.vlsr-vmax)/1e3, vmax=(self.vlsr+vmax)/1e3,
                       cmap=rotationmap.cmap(), zorder=-9)
        cb = plt.colorbar(im, pad=0.03, extend='both', format='%.2f')
        cb.minorticks_on()
        cb.set_label(r'${\rm v_{0} \quad (km\,s^{-1})}$',
                     rotation=270, labelpad=15)
        if ivar is not None:
            ax.contour(self.xaxis, self.yaxis, ivar,
                       [0.0], colors='k')
            ax.contourf(self.xaxis, self.yaxis, ivar,
                        [-1.0, 0.0], colors='k', alpha=0.5)
        self._gentrify_plot(ax)
        if return_fig:
            return fig

    # -- MCMC Functions -- #

    def _optimize_p0(self, theta, params, **kwargs):
        """Optimize the initial starting positions."""
        from scipy.optimize import minimize

        # TODO: implement bounds.
        # TODO: cycle through parameters one at a time for a better fit.

        # Negative log-likelihood function.
        def nlnL(theta):
            return -self._ln_probability(theta, params)

        method = kwargs.pop('method', 'TNC')
        options = kwargs.pop('options', {})
        options['maxiter'] = options.pop('maxiter', 10000)
        options['maxfun'] = options.pop('maxfun', 10000)
        options['ftol'] = options.pop('ftol', 1e-3)

        res = minimize(nlnL, x0=theta, method=method, options=options)
        if res.success:
            theta = res.x
            print("Optimized starting positions:")
        else:
            print("WARNING: scipy.optimize did not converge.")
            print("Starting positions:")
        print('\tp0 =', ['%.2e' % t for t in theta])
        time.sleep(0.3)
        return theta

    def _run_mcmc(self, p0, params, nwalkers, nburnin, nsteps, mcmc, **kwargs):
        """Run the MCMC sampling. Returns the sampler."""

        if mcmc == 'zeus':
            EnsembleSampler = zeus.EnsembleSampler
        else:
            EnsembleSampler = emcee.EnsembleSampler

        p0 = random_p0(p0, kwargs.pop('scatter', 1e-3), nwalkers)
        moves = kwargs.pop('moves', None)
        pool = kwargs.pop('pool', None)

        sampler = EnsembleSampler(nwalkers,
                                  p0.shape[1],
                                  self._ln_probability,
                                  args=[params, np.nan],
                                  moves=moves,
                                  pool=pool)

        progress = kwargs.pop('progress', True)

        sampler.run_mcmc(p0, nburnin + nsteps, progress=progress, **kwargs)

        return sampler

    def _ln_likelihood(self, params):
        """Log-likelihood function. Simple chi-squared likelihood."""
        model = self._make_model(params)
        lnx2 = np.where(self.mask, np.power((self.data - model), 2), 0.0)
        lnx2 = -0.5 * np.sum(lnx2 * self.ivar)
        return lnx2 if np.isfinite(lnx2) else -np.inf

    def _ln_probability(self, theta, *params_in):
        """Log-probablility function."""
        model = rotationmap._populate_dictionary(theta, params_in[0])
        lnp = self._ln_prior(model)
        if np.isfinite(lnp):
            return lnp + self._ln_likelihood(model)
        return -np.inf

    def _set_default_priors(self):
        """Set the default priors."""

        # Basic Geometry.

        self.set_prior('x0', [-0.5, 0.5], 'flat')
        self.set_prior('y0', [-0.5, 0.5], 'flat')
        self.set_prior('inc', [-90.0, 90.0], 'flat')
        self.set_prior('PA', [-360.0, 360.0], 'flat')
        self.set_prior('mstar', [0.1, 5.0], 'flat')
        self.set_prior('vlsr', [np.nanmin(self.data),
                                np.nanmax(self.data)], 'flat')

        # Emission Surface

        self.set_prior('z0', [0.0, 5.0], 'flat')
        self.set_prior('psi', [0.0, 5.0], 'flat')
        self.set_prior('r_cavity', [0.0, 1e30], 'flat')
        self.set_prior('r_taper', [0.0, 1e30], 'flat')
        self.set_prior('q_taper', [0.0, 15.0], 'flat')

        # Warp

        self.set_prior('w_i', [-90.0, 90.0], 'flat')
        self.set_prior('w_r', [-10.0, 10.0], 'flat')
        self.set_prior('w_t', [-180.0, 180.0], 'flat')

        # Velocity Profile

        self.set_prior('vp_100', [0.0, 1e4], 'flat')
        self.set_prior('vp_q', [-2.0, 0.0], 'flat')
        self.set_prior('vp_rtaper', [0.0, 1e30], 'flat')
        self.set_prior('vp_qtaper', [0.0, 5.0], 'flat')
        self.set_prior('vr_100', [-1e3, 1e3], 'flat')
        self.set_prior('vr_q', [-2.0, 2.0], 'flat')
        self.set_prior('r_pressure', [0.0, 3.0*self.xaxis.max()], 'flat')
        self.set_prior('w_pressure', [0.0, 1e2], 'flat')

        # SHO functions.

        self.set_SHO_prior('vrot', [-3e3, 3e3], 'flat')
        self.set_SHO_prior('vrad', [-1e2, 1e2], 'flat')
        self.set_SHO_prior('vlsr', [-1e4, 1e4], 'flat')

    def _ln_prior(self, params):
        """Log-priors."""
        lnp = 0.0
        for key in params.keys():
            if key in rotationmap.priors.keys() and params[key] is not None:
                lnp += rotationmap.priors[key](params[key])
                if not np.isfinite(lnp):
                    return lnp
        return lnp

    def _calc_ivar(self, params):
        """Calculate the inverse variance including radius mask."""

        # Check the error array is the same shape as the data.

        try:
            assert self.error.shape == self.data.shape
        except AttributeError:
            self.error = self.error * np.ones(self.data.shape)

        # Deprojected coordinates.

        r, t = self.disk_coords(**params)[:2]
        t = abs(t) if params['abs_phi'] else t

        # Radial mask.

        mask_r = np.logical_and(r >= params['r_min'], r <= params['r_max'])
        mask_r = ~mask_r if params['exclude_r'] else mask_r

        # Azimuthal mask.

        mask_p = np.logical_and(t >= np.radians(params['phi_min']),
                                t <= np.radians(params['phi_max']))
        mask_p = ~mask_p if params['exclude_phi'] else mask_p

        # Finite value mask.

        mask_f = np.logical_and(np.isfinite(self.data), self.error > 0.0)

        # Velocity mask.

        v_min, v_max = params['v_min'], params['v_max']
        mask_v = np.logical_and(self.data >= v_min, self.data <= v_max)
        mask_v = ~mask_v if params['exclude_v'] else mask_v

        # Combine with the user_mask.

        mask = np.logical_and(np.logical_and(mask_v, mask_f),
                              np.logical_and(mask_r, mask_p))
        mask = np.logical_and(mask, params['user_mask'])
        return np.where(mask, np.power(self.error, -2.0), 0.0)

    @staticmethod
    def _get_labels(params):
        """Return the labels of the parameters to fit."""
        idxs, labs = [], []
        for k in params.keys():
            if isinstance(params[k], int):
                if not isinstance(params[k], bool):
                    idxs.append(params[k])
                    try:
                        idx = k.index('_') + 1
                        label = k[:idx] + '{{' + k[idx:] + '}}'
                    except ValueError:
                        label = k
                    label = r'${{\rm {}}}$'.format(label)
                    labs.append(label)
        return np.array(labs)[np.argsort(idxs)]

    @staticmethod
    def _populate_dictionary(theta, dictionary_in):
        """Populate the dictionary of free parameters."""
        dictionary = dictionary_in.copy()
        for key in dictionary.keys():
            if isinstance(dictionary[key], int):
                if not isinstance(dictionary[key], bool):
                    dictionary[key] = theta[dictionary[key]]
        return dictionary

    def verify_params_dictionary(self, params):
        """
        Check that the minimum number of parameters are provided for the
        fitting. For non-essential parameters a default value is set.
        """

        # Basic geometrical properties.

        params['x0'] = params.pop('x0', 0.0)
        params['y0'] = params.pop('y0', 0.0)
        params['dist'] = params.pop('dist', 100.0)
        params['vlsr'] = params.pop('vlsr', self.vlsr)
        if params.get('inc', None) is None:
            raise KeyError("Must provide `'inc'`.")
        if params.get('PA', None) is None:
            raise KeyError("Must provide `'PA'`.")

        # Rotation profile.

        if params.get('r_pressure') is None:
            params['has_pressure'] = False
        else:
            params['has_pressure'] = True

        if params.get('vp_100') is None:
            params['has_vp_100'] = False
        else:
            params['has_vp_100'] = True

        if params.get('mstar') is None:
            params['has_mstar'] = False
        else:
            params['has_mstar'] = True

        if params['has_mstar'] and params['has_vp_100']:
            raise KeyError("Only provide either `'mstar'` or `'vp_100'`.")
        if not params['has_mstar'] and not params['has_vp_100']:
            raise KeyError("Must provide either `'mstar'` or `'vp_100'`.")
        if params['has_mstar']:
            if params['has_pressure']:
                params['vfunc'] = self._vkep_pressure
            else:
                params['vfunc'] = self._vkep
        else:
            if params['has_pressure']:
                params['vfunc'] = self._vpow_pressure
            else:
                params['vfunc'] = self._vpow

        params['vp_q'] = params.pop('vp_q', -0.5)
        params['vp_rtaper'] = params.pop('vp_rtaper', 1e10)
        params['vp_qtaper'] = params.pop('vp_qtaper', 1.0)
        params['vr_100'] = params.pop('vr_100', 0.0)
        params['vr_q'] = params.pop('vr_q', 0.0)
        params['w_pressure'] = params.pop('w_pressure', 0.0)

        # Flared emission surface.

        params['z0'] = params.pop('z0', 0.0)
        params['psi'] = params.pop('psi', 1.0)
        params['r_taper'] = params.pop('r_taper', None)
        params['q_taper'] = params.pop('q_taper', None)
        params['r_cavity'] = params.pop('r_cavity', None)
        params['z_func'] = params.pop('z_func', None)

        # Warp parameters.

        params['w_i'] = params.pop('w_i', 0.0)
        params['w_r'] = params.pop('w_r', self.dpix)
        params['w_t'] = params.pop('w_t', 0.0)
        params['shadowed'] = params.pop('shadowed', False)

        # Masking parameters.

        params['r_min'] = params.pop('r_min', 0.0)
        params['r_max'] = params.pop('r_max', 1e10)
        params['exclude_r'] = params.pop('exclude_r', False)
        params['phi_min'] = params.pop('phi_min', -180.0)
        params['phi_max'] = params.pop('phi_max', 180.0)
        params['exclude_phi'] = params.pop('exclude_phi', False)
        params['abs_phi'] = params.pop('abs_phi', False)
        params['v_min'] = params.pop('v_min', np.nanmin(self.data))
        params['v_max'] = params.pop('v_max', np.nanmax(self.data))
        params['exclude_v'] = params.pop('exclude_v', False)
        params['user_mask'] = params.pop('user_mask', np.ones(self.data.shape))

        if params['r_min'] >= params['r_max']:
            raise ValueError("`r_max` must be greater than `r_min`.")
        if params['phi_min'] >= params['phi_max']:
            raise ValueError("`phi_max` must be great than `phi_min`.")
        if params['v_min'] >= params['v_max']:
            raise ValueError("`v_max` must be greater than `v_min`.")

        # Beam convolution.

        params['beam'] = bool(params.pop('beam', False))

        return params

    def evaluate_models(self, samples=None, params=None, draws=0.5,
                        collapse_func=np.mean, coords_only=False,
                        profile_only=False):
        """
        Evaluate models based on the samples provided and the parameter
        dictionary. If ``draws`` is an integer, it represents the number of
        random draws from ``samples`` which are then averaged to return the
        model. Alternatively ``draws`` can be a float between 0 and 1,
        representing the percentile of the samples to use to evaluate the model
        at.

        Args:
            samples (ndarray): An array of samples returned from ``fit_map``.
            params (dict): The parameter dictionary passed to ``fit_map``.
            draws (Optional[int/float]): If an integer, describes the number of
                random draws averaged to form the returned model. If a float,
                represents the percentile used from the samples. Must be
                between 0 and 1 if a float.
            collapse_func (Optional[callable]): How to collapse the random
                number of samples. Must be a function which allows an ``axis``
                argument (as with most Numpy functions).
            coords_only (Optional[bool]): Return the deprojected coordinates
                rather than the v0 model. Default is False.
            profile_only (Optional[bool]): Return the radial profiles of the
                velocity profiles rather than the v0 model. Default is False.

        Returns:
            model (ndarray): The sampled model, either the v0 model, or, if
                ``coords_only`` is True, the deprojected cylindrical
                coordinates, (r, t, z).
        """

        # Check the input.

        if params is None:
            raise ValueError("Must provide model parameters dictionary.")

        # Model is fully specified.

        if samples is None:
            verified_params = self.verify_params_dictionary(params.copy())
            if coords_only:
                return self.disk_coords(**verified_params)
            else:
                if profile_only:
                    return self._make_profile(verified_params)
                else:
                    return self._make_model(verified_params)

        nparam = np.sum([type(params[k]) is int for k in params.keys()])
        if samples.shape[1] != nparam:
            warning = "Invalid number of free parameters in 'samples': {:d}."
            raise ValueError(warning.format(nparam))
        if not callable(collapse_func):
            raise ValueError("'collapse_func' must be callable.")
        verified_params = self.verify_params_dictionary(params.copy())

        # Avearge over a random draw of models.

        if isinstance(int(draws) if draws > 1.0 else draws, int):
            rvals, models = [], []
            for idx in np.random.randint(0, samples.shape[0], draws):
                tmp = self._populate_dictionary(samples[idx], verified_params)
                if coords_only:
                    models += [self.disk_coords(**tmp)]
                elif profile_only:
                    _rval, _model = self._make_profile(tmp)
                    rvals += [_rval]
                    models += [_model]
                else:
                    models += [self._make_model(tmp)]
            rvals = collapse_func(rvals, axis=0)
            models = collapse_func(models, axis=0)
            return (rvals, models) if profile_only else models

        # Take a percentile of the samples.

        elif isinstance(draws, float):
            tmp = np.percentile(samples, draws, axis=0)
            tmp = self._populate_dictionary(tmp, verified_params)
            if coords_only:
                return self.disk_coords(**tmp)
            elif profile_only:
                return self._make_profile(tmp)
            else:
                return self._make_model(tmp)

        else:
            raise ValueError("'draws' must be a float or integer.")

    def save_model(self, samples=None, params=None, model=None, filename=None,
                   overwrite=True):
        """
        Save the model as a FITS file. If you have used ``downsample`` when
        loading the cube data, _this will not work_.
        """
        from astropy.io import fits
        if model is None:
            model = self.evaluate_models(samples, params)
        if self.header['naxis1'] > self.nypix:
            canvas = np.ones(self._original_shape) * np.nan
            canvas[self._ya:self._yb, self._xa:self._xb] = model
            model = canvas.copy()
        if filename is None:
            filename = self.path.replace('.fits', '_model.fits')
        fits.writeto(filename, model, self.header, overwrite=overwrite)

    def mirror_residual(self, samples, params, mirror_velocity_residual=True,
                        mirror_axis='minor', return_deprojected=False,
                        deprojected_dpix_scale=1.0):
        """
        Return the residuals after subtracting a mirror image of either the
        rotation map, as in _Huang et al. 2018, or the residuals, as in
        _Izquierdo et al. 2021.

        .. _Huang et al. 2018: https://ui.adsabs.harvard.edu/abs/2018ApJ...867....3H/abstract
        .. _Izquierdo et al. 2021: https://ui.adsabs.harvard.edu/abs/2021arXiv210409530V/abstract

        Args:
            samples (ndarray): An array of samples returned from ``fit_map``.
            params (dict): The parameter dictionary passed to ``fit_map``.
            mirror_velocity_residual (Optional[bool]): If ``True``, the
                default, mirror the velocity residuals, otherwise use the line
                of sight velocity corrected for the systemic velocity.
            mirror_axis (Optional[str]): Which axis to mirror the image along,
                either ``'minor'`` or ``'major'``.
            return_deprojected (Optional[bool]): If ``True``, return the
                deprojected image, or, if ``False``, reproject the data onto
                the sky.

        Returns:
            x, y, residual (array, array, array): The x- and y-axes of the
                residual (either the sky axes or deprojected, depending on the
                chosen arguments) and the residual.
        """

        # Calculate the image to mirror.

        if mirror_velocity_residual:
            to_mirror = self.data * 1e3 - self.evaluate_models(samples, params)
        else:
            to_mirror = self.data.copy() * 1e3
            if isinstance(type(params['vlsr']), int):
                to_mirror -= params['vlsr']
            else:
                to_mirror -= np.median(samples, axis=0)[params['vlsr']]

        # Generate the axes for the deprojected image.

        r, t, _ = self.evaluate_models(samples, params, coords_only=True)
        t += np.pi / 2.0 if mirror_axis.lower() == 'minor' else 0.0
        x = np.nanmax(np.where(np.isfinite(to_mirror), r, np.nan))
        x = np.arange(-x, x, deprojected_dpix_scale * self.dpix)
        x -= 0.5 * (x[0] + x[-1])

        xs = (r * np.cos(t)).flatten()
        ys = (r * np.sin(t)).flatten()

        # Deproject the image.

        from scipy.interpolate import griddata
        d = griddata((xs, ys), to_mirror.flatten(), (x[:, None], x[None, :]))

        # Either subtract or add the mirrored image. Only want to add when
        # mirroring the line-of-sight velocity and mirroring about the minor
        # axis.

        if not mirror_velocity_residual and mirror_axis == 'minor':
            d += d[:, ::-1]
        else:
            d -= d[:, ::-1]

        if return_deprojected:
            return x, x, d

        # Reproject the residuals onto the sky plane.

        dd = d.flatten()
        mask = np.isfinite(dd)
        xx, yy = np.meshgrid(x, x)
        xx, yy = xx.flatten(), yy.flatten()
        xx, yy, dd = xx[mask], yy[mask], dd[mask]

        from scipy.interpolate import interp2d

        f = interp2d(xx, yy, dd, kind='linear')
        f = np.squeeze([f(xd, yd) for xd, yd in zip(xs, ys)])
        f = f.reshape(to_mirror.shape)
        f = np.where(np.isfinite(to_mirror), f, np.nan)

        return self.xaxis, self.yaxis, f

    # -- VELOCITY PROJECTION -- #

    def _vkep(self, rvals, tvals, zvals, params):
        """Keplerian rotation velocity."""
        r_m = rvals * sc.au * params['dist']
        z_m = zvals * sc.au * params['dist']
        vkep = sc.G * params['mstar'] * self.msun * np.power(r_m, 2)
        return np.sqrt(vkep * np.power(np.hypot(r_m, z_m), -3))

    def _vkep_pressure(self, rvals, tvals, zvals, params):
        """Keplerian rotation velocity with pressure term."""
        vkep = self._vkep(rvals, tvals, zvals, params)
        r_p = params['r_pressure']
        idx = np.unravel_index(abs(rvals - r_p).argmin(), rvals.shape)
        dvprs = (1.0 - 1.5 * r_p**2 / (r_p**2 + zvals[idx]**2))
        dvprs = ((rvals - r_p) / r_p) * dvprs + 1.0
        vkep = np.where(rvals <= r_p, vkep, vkep[idx] * dvprs)
        vkep = np.clip(vkep, a_min=0.0, a_max=None)
        if params['w_pressure'] > 0.0:
            taper = (rvals - r_p) / params['w_pressure']
            taper = np.exp(-np.power(taper, 2.0))
            vkep *= np.where(rvals <= r_p, 1.0, taper)
        return vkep

    def _vpow(self, rvals, tvals, zvals, params):
        """Power-law rotation velocity profile."""
        vpow = (rvals * params['dist'] / 100.)**params['vp_q']
        return params['vp_100'] * vpow

    def _vpow_pressure(self, rvals, tvals, zvals, params):
        """Power-law rotation with pressure term."""
        vpow = self._vpow(rvals, tvals, zvals, params)
        r_p = params['r_pressure']
        idx = np.unravel_index(abs(rvals - r_p).argmin(), rvals.shape)
        dvprs = ((rvals - r_p) / r_p) * params['vp_q'] + 1.0
        vpow = np.where(rvals <= r_p, vpow, vpow[idx] * dvprs)
        if params['w_pressure'] > 0.0:
            taper = (rvals - r_p) / params['w_pressure']
            taper = np.exp(-np.power(taper, 2.0))
            vpow *= np.where(rvals <= r_p, 1.0, taper)
        return vpow

    def _proj_vphi(self, v_phi, tvals, params):
        """Project the rotational velocity onto the sky."""
        return v_phi * np.cos(tvals) * np.sin(abs(np.radians(params['inc'])))

    def _proj_vrad(self, v_rad, tvals, params):
        """Project the radial velocity onto the sky."""
        return v_rad * np.sin(tvals) * np.sin(-np.radians(params['inc']))

    def _proj_valt(self, v_alt, tvals, params):
        """Project the vertical velocity onto the sky."""
        return -v_alt * np.cos(np.radians(params['inc']))

    def _make_model(self, params):
        """Build the velocity model from the dictionary of parameters."""
        rvals, tvals, zvals = self.disk_coords(**params)
        vphi = params['vfunc'](rvals, tvals, zvals, params)
        v0 = self._proj_vphi(vphi, tvals, params) + params['vlsr']
        if params['beam']:
            v0 = datacube._convolve_image(v0, self._beamkernel())
        return v0

    def _make_profile(self, params):
        """Build the velocity profile from the dictionary of parameters."""
        rvals, _, zvals = self.disk_coords(**params)
        rvals, zvals = rvals.flatten(), zvals.flatten()
        idx = np.argsort(rvals)
        rvals, zvals = rvals[idx], zvals[idx]
        tvals = np.zeros(rvals.size)
        return rvals, params['vfunc'](rvals, tvals, zvals, params)

    def deproject_model_residuals(self, samples, params):
        """
        Deproject the residuals into cylindrical velocity components. Takes the
        median value of the samples to determine the model.

        Args:
            samples (ndarray): An array of samples returned from ``fit_map``.
            params (dict): The parameter dictionary passed to ``fit_map``.
        """
        median_samples = np.median(samples, axis=0)
        verified_params = self.verify_params_dictionary(params.copy())
        model = self._populate_dictionary(median_samples, verified_params)
        v_res = self.data - self._make_model(model)
        rvals, tvals, zvals = self.disk_coords(**model)
        v_p = v_res / np.cos(tvals) / np.sin(-np.radians(model['inc']))
        v_r = v_res / np.sin(tvals) / np.sin(abs(np.radians(model['inc'])))
        v_z = v_res / np.cos(abs(np.radians(model['inc'])))
        v_z = np.where(zvals >= 0.0, -v_z, v_z)
        return v_p, v_r, v_z

    # -- Functions to help determine the emission height. -- #

    def find_maxima(self, x0=0.0, y0=0.0, PA=0.0, vlsr=None, r_max=None,
                    r_min=None, smooth=False, through_center=True):
        """
        Find the node of velocity maxima along the major axis of the disk.

        Args:
            x0 (Optional[float]): Source center offset along x-axis in
                [arcsec].
            y0 (Optional[float]): Source center offset along y-axis in
                [arcsec].
            PA (Optioanl[float]): Source position angle in [deg].
            vlsr (Optional[float]): Systemic velocity in [m/s].
            r_max (Optional[float]): Maximum offset to consider in [arcsec].
            r_min (Optional[float]): Minimum offset to consider in [arcsec].
            smooth (Optional[bool/float]): Smooth the line of nodes. If
                ``True``, smoth with the beam kernel, otherwise ``smooth``
                describes the FWHM of the Gaussian convolution kernel in
                [arcsec].
            through_center (Optional[bool]): If ``True``, force the central
                pixel to go through ``(0, 0)``.

        Returns:
            array, array: Arrays of ``x_sky`` and ``y_sky`` values of the
            maxima.
        """

        # Default parameters.
        vlsr = np.nanmedian(self.data) if vlsr is None else vlsr
        r_max = 0.5 * self.xaxis.max() if r_max is None else r_max
        r_min = 0.0 if r_min is None else r_min

        # Shift and rotate the image.
        data = self._shift_center(dx=x0, dy=y0, save=False)
        data = self._rotate_image(PA=PA, data=data, save=False)

        # Find the maximum values. Apply some clipping to help.
        mask = np.maximum(0.3 * abs(self.xaxis), self.bmaj)
        mask = abs(self.yaxis)[:, None] > mask[None, :]
        resi = np.where(mask, 0.0, abs(data - vlsr))
        resi = np.take(self.yaxis, np.argmax(resi, axis=0))

        # Gentrification.
        if through_center:
            resi[abs(self.xaxis).argmin()] = 0.0
        if smooth:
            if isinstance(smooth, bool):
                kernel = np.hanning(self.bmaj / self.dpix)
                kernel /= kernel.sum()
            else:
                from astropy.convolution import Gaussian1DKernel
                kernel = Gaussian1DKernel(smooth / self.fwhm / self.dpix)
            resi = np.convolve(resi, kernel, mode='same')
        mask = np.logical_and(abs(self.xaxis) <= r_max,
                              abs(self.xaxis) >= r_min)
        x, y = self.xaxis[mask], resi[mask]

        # Rotate back to sky-plane and return.
        x, y = self._rotate_coords(x, -y, PA)
        return x + x0, y + y0

    def find_minima(self, x0=0.0, y0=0.0, PA=0.0, vlsr=None, r_max=None,
                    r_min=None, smooth=False, through_center=True):
        """
        Find the line of nodes where v0 = v_LSR along the minor axis.

        Args:
            x0 (Optional[float]): Source center offset along x-axis in
                [arcsec].
            y0 (Optional[float]): Source center offset along y-axis in
                [arcsec].
            PA (Optioanl[float]): Source position angle in [deg].
            vlsr (Optional[float]): Systemic velocity in [m/s].
            r_max (Optional[float]): Maximum offset to consider in [arcsec].
            r_min (Optional[float]): Minimum offset to consider in [arcsec].
            smooth (Optional[bool/float]): Smooth the line of nodes. If
                ``True``, smoth with the beam kernel, otherwise ``smooth``
                describes the FWHM of the Gaussian convolution kernel in
                [arcsec].
            through_center (Optional[bool]): If ``True``, force the central
                pixel to go through ``(0, 0)``.

        Returns:
            array, array: Arrays of ``x_sky`` and ``y_sky`` values of the
            velocity minima.
        """

        # Default parameters.
        vlsr = np.nanmedian(self.data) if vlsr is None else vlsr
        r_max = 0.5 * self.xaxis.max() if r_max is None else r_max
        r_min = 0.0 if r_min is None else r_min

        # Shift and rotate the image.
        data = self._shift_center(dx=x0, dy=y0, save=False)
        data = self._rotate_image(PA=PA, data=data, save=False)

        # Find the maximum values. Apply some clipping to help.
        mask = np.maximum(0.3 * abs(self.yaxis), self.bmaj)
        mask = abs(self.xaxis)[None, :] > mask[:, None]
        resi = np.where(mask, 1e10, abs(data - vlsr))
        resi = np.take(-self.yaxis, np.argmin(resi, axis=1))

        # Gentrification.
        if through_center:
            resi[abs(self.yaxis).argmin()] = 0.0
        if smooth:
            if isinstance(smooth, bool):
                kernel = np.hanning(self.bmaj / self.dpix)
                kernel /= kernel.sum()
            else:
                from astropy.convolution import Gaussian1DKernel
                kernel = Gaussian1DKernel(smooth / self.fwhm / self.dpix)
            resi = np.convolve(resi, kernel, mode='same')
        mask = np.logical_and(abs(self.yaxis) <= r_max,
                              abs(self.yaxis) >= r_min)
        x, y = resi[mask], self.yaxis[mask]

        # Rotate back to sky-plane and return.
        x, y = self._rotate_coords(x, -y, PA)
        return x + x0, y + y0

    def _fit_surface(self, inc, PA, x0=None, y0=None, r_min=None, r_max=None,
                     fit_z1=False, ycut=20.0, **kwargs):
        """
        Fit the emission surface with the parametric model based on the pixels
        of peak velocity.

        Args:
            inc (float): Disk inclination in [degrees].
            PA (float): Disk position angle in [degrees].
            x0 (Optional[float]): Disk center x-offset in [arcsec].
            y0 (Optional[float]): Disk center y-offset in [arcsec].
            r_min (Optional[float]): Minimum radius to fit in [arcsec].
            r_max (Optional[float]): Maximum radius to fit in [arcsec].
            fit_z1 (Optional[bool]): Include (z1, phi) in the fit.
            y_cut (Optional[float]): Only use the `ycut` fraction of the minor
                axis for fitting.
            kwargs (Optional[dict]): Additional kwargs for curve_fit.

        Returns:
            popt (list): Best-fit parameters of (z0, psi[, z1, phi]).
        """

        from scipy.optimize import curve_fit

        def z_func(x, z0, psi, z1=0.0, phi=1.0):
            return z0 * x**psi + z1 * x**phi

        # Get the coordinates to fit.
        r, z = self.get_peak_pix(PA=PA, inc=inc, x0=x0, y0=y0,
                                 frame='disk', ycut=ycut)

        # Mask the coordinates.
        r_min = r_min if r_min is not None else r[0]
        r_max = r_max if r_max is not None else r[-1]
        m1 = np.logical_and(np.isfinite(r), np.isfinite(z))
        m2 = (r >= r_min) & (r <= r_max)
        mask = m1 & m2
        r, z = r[mask], z[mask]

        # Initial guesses for the free params.
        p0 = [z[abs(r - 1.0).argmin()], 1.0]
        if fit_z1:
            p0 += [-0.05, 3.0]
        maxfev = kwargs.pop('maxfev', 100000)

        # First fit the inner half to get a better p0 value.
        mask = r <= 0.5 * r.max()
        p_in = curve_fit(z_func, r[mask], z[mask], p0=p0, maxfev=maxfev,
                         **kwargs)[0]

        # Remove the pixels which are 'negative' depending on the inclination.
        mask = z > 0.0 if np.sign(p_in[0]) else z < 0.0
        popt = curve_fit(z_func, r[mask], z[mask], p0=p_in, maxfev=maxfev,
                         **kwargs)[0]
        return popt

    # -- Axes Functions -- #

    def downsample_cube(self, N, randomize=False):
        """Downsample the cube to make faster calculations."""
        N = int(np.ceil(self.bmaj / self.dpix)) if N == 'beam' else N
        if randomize:
            N0x, N0y = np.random.randint(0, N, 2)
        else:
            N0x, N0y = int(N / 2), int(N / 2)
        if N > 1:
            self.xaxis = self.xaxis[N0x::N]
            self.yaxis = self.yaxis[N0y::N]
            self.data = self.data[N0y::N, N0x::N]
            self.error = self.error[N0y::N, N0x::N]
            self.mask = self.mask[N0y::N, N0x::N]

    def _shift_center(self, dx=0.0, dy=0.0, data=None, save=True):
        """
        Shift the center of the image.

        Args:
            dx (optional[float]): shift along x-axis [arcsec].
            dy (optional[float]): Shift along y-axis [arcsec].
            data (optional[ndarray]): Data to shift. If nothing is provided,
                will shift the attached ``rotationmap.data``.
            save (optional[bool]): If True, overwrite ``rotationmap.data``.
        """
        from scipy.ndimage import shift
        data = self.data.copy() if data is None else data
        to_shift = np.where(np.isfinite(data), data, 0.0)
        data = shift(to_shift, [-dy / self.dpix, dx / self.dpix])
        if save:
            self.data = data
        return data

    def _rotate_image(self, PA, data=None, save=True):
        """
        Rotate the image anticlockwise about the center.

        Args:
            PA (float): Rotation angle in [degrees].
            data (optional[ndarray]): Data to shift. If nothing is provided,
                will shift the attached ``rotationmap.data``.
            save (optional[bool]): If True, overwrite ``rotationmap.data``.
        """
        from scipy.ndimage import rotate
        data = self.data.copy() if data is None else data
        to_rotate = np.where(np.isfinite(data), data, 0.0)
        data = rotate(to_rotate, PA - 90.0, reshape=False)
        if save:
            self.data = data
        return data

    # -- DATA I/O -- #

    def _readuncertainty(self, uncertainty, FOV=None):
        """Reads the uncertainties."""
        if uncertainty is not None:
            self.error = datacube(uncertainty, FOV=FOV, fill=None)
            self.error = self.error.data.copy()
        else:
            try:
                uncertainty = '_'.join(self.path.split('_')[:-1])
                uncertainty += '_d' + self.path.split('_')[-1]
                print("Assuming uncertainties in {}.".format(uncertainty))
                self.error = datacube(uncertainty, FOV=FOV, fill=None)
                self.error = self.error.data.copy()
            except FileNotFoundError:
                print("No uncertainties found, assuming uncertainties of 10%.")
                print("Change this at any time with `rotationmap.error`.")
                self.error = 0.1 * (self.data - np.nanmedian(self.data))
        self.error = np.where(np.isnan(self.error), 0.0, abs(self.error))
        self.error *= 1e3 if self.velocity_unit == 'km/s' else 1.0
        assert self.data.shape == self.error.shape

    # -- PLOTTING -- #

    def plot_velocity_profiles(self, rpnts, fits, uncertainty, fit_vrot=True,
                               fit_vrad=True, fix_vlsr=False):
        """
        Plot the velocity profiles.

        Args:
            rpnts (array): Array of the annulus centers.
            fits (ndarray): Array of the velocity profiles with a shape of
                ``(nparam, nannuli)``.
            uncertainy (ndarray): Array of the uncertainties of the velocity
                profiles with the same shape as ``fits``.
            fit_vrot (Optional[bool]): Whether to include rotational velocities
                in the fit. Default is ``True``.
            fit_vrad (Optional[bool]): Whether to include radial velocities in
                    the fit. Default is ``True``.
            fix_vlsr (bool/float): Whether the system velocity was fixed (and
                so should be a ``float``), or if it was left free (``False``).
        """

        # Unpack the velocity profiles. If parameters are fixed, their
        # uncertainties are NaNs.

        idx = 0
        if fit_vrot:
            v_phi, dv_phi = fits[idx], uncertainty[idx]
            mu = np.nanmedian(v_phi)
            std = np.nanpercentile(v_phi, [16, 84])
            std = 0.5 * (std[1] - std[0])
            v_phi_ylim = np.nanpercentile(v_phi, [2, 98])
            idx += 1
        else:
            v_phi = np.zeros(fits.shape[-1])
            dv_phi = v_phi.copy() * np.nan
            v_phi_ylim = None

        if fit_vrad:
            v_rad, dv_rad = fits[idx], uncertainty[idx]
            mu = np.nanmedian(v_rad)
            std = np.nanpercentile(v_rad, [16, 84])
            std = 0.5 * (std[1] - std[0])
            v_rad_ylim = (mu - 3.0 * std, mu + 3.0 * std)
            idx += 1
        else:
            v_rad = np.zeros(fits.shape[-1])
            dv_rad = v_rad.copy() * np.nan
            v_rad_ylim = None

        if not fix_vlsr:
            v_lsr, dv_lsr = fits[idx], uncertainty[idx]
            mu = np.nanmedian(v_lsr)
            std = np.nanpercentile(v_lsr, [16, 84])
            std = 0.5 * (std[1] - std[0])
            v_lsr_ylim = (mu - 3.0 * std, mu + 3.0 * std)
        else:
            v_lsr = np.ones(v_phi.size) * fix_vlsr
            dv_lsr = np.ones(v_phi.size) * np.nan
            v_lsr_ylim = None

        # Make the axes.

        fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(6.75, 6.25))
        axs[0].errorbar(rpnts, v_phi, dv_phi, fmt='-o', ms=3)
        axs[0].set_xlabel(r'Radius (arcsec)', labelpad=8)
        axs[0].xaxis.set_label_position('top')
        axs[0].xaxis.tick_top()
        axs[0].set_ylabel(r'$v_{\rm \phi,\, proj}$' + ' (m/s)')
        axs[0].set_ylim(v_phi_ylim)

        axs[1].errorbar(rpnts, v_rad, dv_rad, fmt='-o', ms=3)
        axs[1].set_xticklabels([])
        axs[1].set_ylabel(r'$v_{\rm rad,\, proj}$' + ' (m/s)')
        axs[1].set_ylim(v_rad_ylim)

        axs[2].errorbar(rpnts, v_lsr, dv_lsr, fmt='-o', ms=3)
        axs[2].set_xlabel(r'Radius (arcsec)')
        axs[2].set_ylabel(r'$v_{\rm lsr}$' + ' (m/s)')
        axs[2].set_ylim(v_lsr_ylim)

        for ax in axs:
            ax.grid(ls='--', color='0.9', lw=1.0)
            ax.set_xlim(rpnts.min(), rpnts.max())
            ax.tick_params(which='both', bottom=True, right=True, top=True)
        fig.align_labels(axs)

    def plot_model(self, samples=None, params=None, model=None, draws=0.5,
                   mask=None, ax=None, imshow_kwargs=None, cb_label=None,
                   return_fig=False):
        """
        Plot a v0 model using the same scalings as the plot_data() function.

        Args:
            samples (Optional[ndarray]): An array of samples returned from
                ``fit_map``.
            params (Optional[dict]): The parameter dictionary passed to
                ``fit_map``.
            model (Optional[ndarry]): A model array from ``evaluate_models``.
            draws (Optional[int/float]): If an integer, describes the number of
                random draws averaged to form the returned model. If a float,
                represents the percentile used from the samples. Must be
                between 0 and 1 if a float.
            mask (Optional[ndarray]): The mask used for the fitting to plot as
                a shaded region.
            ax (Optional[AxesSubplot]): Axis to plot onto.
            imshow_kwargs (Optional[dict]): Dictionary of imshow kwargs.
            cb_label (Optional[str]): Colorbar label.
            return_fig (Optional[bool]): Return the figure.

        Returns:
            fig (Matplotlib figure): If ``return_fig`` is ``True``. Can access
                the axes through ``fig.axes`` for additional plotting.
        """

        # Dummy axis for the plotting.

        if ax is None:
            fig, ax = plt.subplots()

        # Make the model and calculate the plotting limits.

        if model is None:
            model = self.evaluate_models(samples, params.copy(), draws=draws)
        vmin, vmax = np.nanpercentile(model, [2, 98])
        vmax = max(abs(vmin - self.vlsr), abs(vmax - self.vlsr))
        vmin = self.vlsr - vmax
        vmax = self.vlsr + vmax

        # Initialize the plotting parameters.

        imshow_kwargs = {} if imshow_kwargs is None else imshow_kwargs
        imshow_kwargs['cmap'] = imshow_kwargs.pop('cmap', datacube.cmap())
        imshow_kwargs['zorder'] = imshow_kwargs.pop('zorder', -9)
        imshow_kwargs['extent'] = self.extent
        imshow_kwargs['origin'] = 'lower'
        imshow_kwargs['vmin'] = imshow_kwargs.pop('vmin', vmin)
        imshow_kwargs['vmax'] = imshow_kwargs.pop('vmax', vmax)
        im = ax.imshow(model, **imshow_kwargs)

        # Overplot the mask if necessary.

        if mask is not None:
            ax.contour(self.xaxis, self.yaxis, mask,
                       [0.0], colors='k')
            ax.contourf(self.xaxis, self.yaxis, mask,
                        [-1.0, 0.0], colors='k', alpha=0.5)

        if cb_label is None:
            cb_label = r'${\rm v_{0} \quad (m\,s^{-1})}$'
        if cb_label != '':
            cb = plt.colorbar(im, pad=0.03, format='%.2f', extend='both')
            cb.set_label(cb_label, rotation=270, labelpad=15)
            cb.minorticks_on()

        self._gentrify_plot(ax)

        if return_fig:
            return fig

    def plot_model_residual(self, samples=None, params=None, model=None,
                            draws=0.5, mask=None, ax=None, imshow_kwargs=None,
                            return_fig=False):
        """
        Plot the residual from the provided model.

        Args:
            samples (Optional[ndarray]): An array of samples returned from
                ``fit_map``.
            params (Optional[dict]): The parameter dictionary passed to
                ``fit_map``.
            model (Optional[ndarry]): A model array from ``evaluate_models``.
            draws (Optional[int/float]): If an integer, describes the number of
                random draws averaged to form the returned model. If a float,
                represents the percentile used from the samples. Must be
                between 0 and 1 if a float.
            mask (Optional[ndarray]): The mask used for the fitting to plot as
                a shaded region.
            ax (Optional[AxesSubplot]): Axis to plot onto.
            imshow_kwargs (Optional[dict]): Dictionary of imshow kwargs.
            return_fig (Optional[bool]): Return the figure.

        Returns:
            fig (Matplotlib figure): If ``return_fig`` is ``True``. Can access
                the axes through ``fig.axes`` for additional plotting.
        """

        # Dummy axis to overplot.

        if ax is None:
            fig, ax = plt.subplots()

        # Make the model and calculate the plotting limits.

        if model is None:
            model = self.evaluate_models(samples, params.copy(), draws=draws)
        vres = self.data - model
        mask = np.ones(vres.shape) if mask is None else mask
        masked_vres = np.where(mask, vres, np.nan)
        vmin, vmax = np.nanpercentile(masked_vres, [2, 98])
        vmax = max(abs(vmin), abs(vmax))

        # Plot the data.

        imshow_kwargs = {} if imshow_kwargs is None else imshow_kwargs
        imshow_kwargs['origin'] = 'lower'
        imshow_kwargs['extent'] = self.extent
        imshow_kwargs['cmap'] = 'RdBu_r'
        imshow_kwargs['vmin'] = imshow_kwargs.pop('vmin', -vmax)
        imshow_kwargs['vmax'] = imshow_kwargs.pop('vmax', vmax)
        im = ax.imshow(vres, **imshow_kwargs)

        # Overplot the mask is necessary.

        if mask is not None:
            ax.contour(self.xaxis, self.yaxis, mask,
                       [0.0], colors='k')
            ax.contourf(self.xaxis, self.yaxis, mask,
                        [-1.0, 0.0], colors='k', alpha=0.5)

        cb = plt.colorbar(im, pad=0.02, format='%d', ax=ax, extend='both')
        cb.set_label(r'${\rm  v_{0} - v_{mod} \quad (m\,s^{-1})}$',
                     rotation=270, labelpad=15)
        cb.minorticks_on()

        self._gentrify_plot(ax)

        if return_fig:
            return fig

    def plot_model_surface(self, samples, params,  plot_surface_kwargs=None,
                           mask_with_data=True, return_fig=True):
        """
        Overplot the emission surface onto the provided axis. Takes the median
        value of the samples as the model to plot.

        Args:
            samples (ndarray): An array of samples returned from ``fit_map``.
            params (dict): The parameter dictionary passed to ``fit_map``.
            plot_surface_kwargs (Optional[dict]): Dictionary of kwargs to pass
                to ``plot_surface``.
            mask_with_data (Optional[bool]): If ``True``, mask the surface to
                regions where the data is finite valued.
            return_fig (Optional[bool]): Return the figure.

        Returns:
            fig (Matplotlib figure): If ``return_fig`` is ``True``. Can access
                the axes through ``fig.axes`` for additional plotting.
        """

        # Check the input.

        nparam = np.sum([type(params[k]) is int for k in params.keys()])
        if samples.shape[1] != nparam:
            warning = "Invalid number of free parameters in 'samples': {:d}."
            raise ValueError(warning.format(nparam))
        if plot_surface_kwargs is None:
            plot_surface_kwargs = {}
        plot_surface_kwargs['return_fig'] = True

        # Populate the model with the median values.

        model = self.verify_params_dictionary(params.copy())
        model = self._populate_dictionary(np.median(samples, axis=0), model)
        model['mask'] = np.isfinite(self.data) if mask_with_data else None
        model.pop('r_max')
        fig = self.plot_surface(**model, **plot_surface_kwargs)
        self._gentrify_plot(ax=fig.axes[0])

        if return_fig:
            return fig

    def plot_disk_axes(self, x0=0.0, y0=0.0, inc=0.0, PA=0.0, major=1.0,
                       ax=None, plot_kwargs=None, return_ax=True):
        """
        Plot the major and minor axes on the provided axis.

        Args:
            ax (Matplotlib axes): Axes instance to plot onto.
            x0 (Optional[float]): Relative x-location of the center [arcsec].
            y0 (Optional[float]): Relative y-location of the center [arcsec].
            inc (Optional[float]): Inclination of the disk in [degrees].
            PA (Optional[float]): Position angle of the disk in [degrees].
            major (Optional[float]): Size of the major axis line in [arcsec].
            plot_kwargs (Optional[dict]): Dictionary of parameters to pass to
                ``matplotlib.plot``.

        Returns:
            matplotlib axis: Matplotlib ax with axes drawn.
        """

        # Dummy axis to plot.

        if ax is None:
            fig, ax = plt.subplots()

        x = np.array([major, -major,
                      0.0, 0.0])
        y = np.array([0.0, 0.0,
                      major * np.cos(np.radians(inc)),
                      -major * np.cos(np.radians(inc))])
        x, y = self._rotate_coords(x, y, PA=PA)
        x, y = x + x0, y + y0
        plot_kwargs = {} if plot_kwargs is None else plot_kwargs
        c = plot_kwargs.pop('c', plot_kwargs.pop('color', 'k'))
        ls = plot_kwargs.pop('ls', plot_kwargs.pop('linestyle', ':'))
        lw = plot_kwargs.pop('lw', plot_kwargs.pop('linewidth', 1.0))
        ax.plot(x[:2], y[:2], c=c, ls=ls, lw=lw)
        ax.plot(x[2:], y[2:], c=c, ls=ls, lw=lw)

        if return_ax:
            ax

    def plot_maxima(self, x0=0.0, y0=0.0, inc=0.0, PA=0.0, vlsr=None,
                    r_max=1.0, r_min=None, smooth=False, through_center=True,
                    plot_axes_kwargs=None, plot_kwargs=None,
                    return_fig=False):
        """
        Mark the position of the maximum velocity as a function of radius. This
        can help demonstrate if there is an appreciable bend in velocity
        contours indicative of a flared emission surface. This function pulls
        the results from fit_cube.get_peak_pix() for plotting.

        Args:
            x0 (Optional[float]): Source center x-offset in [arcsec].
            y0 (Optional[float]): Source center y-offset in [arcsec].
            inc (Optional[float]): Disk inclination in [degrees].
            PA (Optional[float]): Disk position angle in [degrees].
            vlsr (Optional[float]): Systemic velocity in [m/s].
            r_max (Optional[float]): Maximum offset to consider in [arcsec].
            r_min (Optional[float]): Minimum offset to consider in [arcsec].
                This is useful to skip large regions where beam convolution
                dominates the map.
            smooth (Optional[bool/float]): Smooth the line of nodes. If
                ``True``, smoth with the beam kernel, otherwise ``smooth``
                describes the FWHM of the Gaussian convolution kernel in
                [arcsec].
            through_center (Optional[bool]): If ``True``, force the central
                pixel to go through ``(0, 0)``.
            levels (Optional[array]): Levels to pass to ``plot_data``.
            plot_axes_kwargs (Optional[dict]): Dictionary of kwargs for the
                plot_axes function.
            plot_kwargs (Optional[dict]): Dictionary of kwargs for the
                plot of the maximum and minimum pixels.
            return_fig (Optional[bool]): If True, return the figure.

        Returns:
            (Matplotlib figure): If return_fig is ``True``. Can access the axis
                through ``fig.axes[0]``.
        """

        # Background figure.
        fig = self.plot_data(return_fig=True)
        ax = fig.axes[0]
        if plot_axes_kwargs is None:
            plot_axes_kwargs = dict()
        self.plot_disk_axes(ax=ax, x0=x0, y0=y0, inc=inc, PA=PA,
                            major=plot_axes_kwargs.pop('major', r_max),
                            **plot_axes_kwargs)

        # Get the pixels for the maximum and minimum values.
        x_maj, y_maj = self.find_maxima(x0=x0, y0=y0, PA=PA, vlsr=vlsr,
                                        r_max=r_max, r_min=r_min,
                                        smooth=smooth,
                                        through_center=through_center)
        r_max = r_max * np.cos(np.radians(inc))
        x_min, y_min = self.find_minima(x0=x0, y0=y0, PA=PA, vlsr=vlsr,
                                        r_max=r_max, r_min=r_min,
                                        smooth=smooth,
                                        through_center=through_center)

        # Plot the lines.
        plot_kwargs = {} if plot_kwargs is None else plot_kwargs
        c = plot_kwargs.pop('c', plot_kwargs.pop('color', 'k'))
        lw = plot_kwargs.pop('lw', plot_kwargs.pop('linewidth', 1.0))

        ax.plot(x_maj, y_maj, c=c, lw=lw, **plot_kwargs)
        ax.plot(x_min, y_min, c=c, lw=lw, **plot_kwargs)

        if return_fig:
            return fig
