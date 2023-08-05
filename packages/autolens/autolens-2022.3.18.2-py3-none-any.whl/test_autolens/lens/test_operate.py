from astropy import cosmology as cosmo
import numpy as np
import pytest
import os
from os import path
import shutil
from skimage import measure

import autolens as al

test_path = path.join("{}".format(path.dirname(path.realpath(__file__))), "files")


def test__operate_image__blurred_images_2d_via_psf_from__for_tracer_gives_list_of_planes(
    sub_grid_2d_7x7, blurring_grid_2d_7x7, psf_3x3
):
    g0 = al.Galaxy(
        redshift=0.5,
        light_profile=al.lp.EllSersic(intensity=1.0),
        mass_profile=al.mp.SphIsothermal(einstein_radius=1.0),
    )
    g1 = al.Galaxy(redshift=1.0, light_profile=al.lp.EllSersic(intensity=2.0))

    plane_0 = al.Plane(redshift=0.5, galaxies=[g0])
    plane_1 = al.Plane(redshift=1.0, galaxies=[g1])

    blurred_image_0 = plane_0.blurred_image_2d_via_psf_from(
        grid=sub_grid_2d_7x7, psf=psf_3x3, blurring_grid=blurring_grid_2d_7x7
    )

    source_grid_2d_7x7 = plane_0.traced_grid_from(grid=sub_grid_2d_7x7)
    source_blurring_grid_2d_7x7 = plane_0.traced_grid_from(grid=blurring_grid_2d_7x7)

    blurred_image_1 = plane_1.blurred_image_2d_via_psf_from(
        grid=source_grid_2d_7x7, psf=psf_3x3, blurring_grid=source_blurring_grid_2d_7x7
    )

    tracer = al.Tracer(planes=[plane_0, plane_1], cosmology=cosmo.Planck15)

    blurred_image = tracer.blurred_image_2d_via_psf_from(
        grid=sub_grid_2d_7x7, psf=psf_3x3, blurring_grid=blurring_grid_2d_7x7
    )

    assert blurred_image.native == pytest.approx(
        blurred_image_0.native + blurred_image_1.native, 1.0e-4
    )

    blurred_image_list = tracer.blurred_image_2d_list_via_psf_from(
        grid=sub_grid_2d_7x7, psf=psf_3x3, blurring_grid=blurring_grid_2d_7x7
    )

    assert (blurred_image_list[0].slim == blurred_image_0.slim).all()
    assert (blurred_image_list[1].slim == blurred_image_1.slim).all()

    assert (blurred_image_list[0].native == blurred_image_0.native).all()
    assert (blurred_image_list[1].native == blurred_image_1.native).all()


def test__operate_image__blurred_images_2d_via_convolver_from__for_tracer_gives_list_of_planes(
    sub_grid_2d_7x7, blurring_grid_2d_7x7, convolver_7x7
):
    g0 = al.Galaxy(
        redshift=0.5,
        light_profile=al.lp.EllSersic(intensity=1.0),
        mass_profile=al.mp.SphIsothermal(einstein_radius=1.0),
    )
    g1 = al.Galaxy(redshift=1.0, light_profile=al.lp.EllSersic(intensity=2.0))

    plane_0 = al.Plane(redshift=0.5, galaxies=[g0])
    plane_1 = al.Plane(redshift=1.0, galaxies=[g1])

    blurred_image_0 = plane_0.blurred_image_2d_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )

    source_grid_2d_7x7 = plane_0.traced_grid_from(grid=sub_grid_2d_7x7)
    source_blurring_grid_2d_7x7 = plane_0.traced_grid_from(grid=blurring_grid_2d_7x7)

    blurred_image_1 = plane_1.blurred_image_2d_via_convolver_from(
        grid=source_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=source_blurring_grid_2d_7x7,
    )

    tracer = al.Tracer(planes=[plane_0, plane_1], cosmology=cosmo.Planck15)

    blurred_image = tracer.blurred_image_2d_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )

    assert blurred_image.native == pytest.approx(
        blurred_image_0.native + blurred_image_1.native, 1.0e-4
    )

    blurred_image_list = tracer.blurred_image_2d_list_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )

    assert (blurred_image_list[0].slim == blurred_image_0.slim).all()
    assert (blurred_image_list[1].slim == blurred_image_1.slim).all()

    assert (blurred_image_list[0].native == blurred_image_0.native).all()
    assert (blurred_image_list[1].native == blurred_image_1.native).all()


def test__operate_image__visibilities_of_planes_from_grid_and_transformer(
    sub_grid_2d_7x7, transformer_7x7_7
):

    g0 = al.Galaxy(redshift=0.5, light_profile=al.lp.EllSersic(intensity=1.0))
    g1 = al.Galaxy(redshift=1.0, light_profile=al.lp.EllSersic(intensity=2.0))

    plane_0 = al.Plane(redshift=0.5, galaxies=[g0])
    plane_1 = al.Plane(redshift=0.5, galaxies=[g1])
    plane_2 = al.Plane(redshift=1.0, galaxies=[al.Galaxy(redshift=1.0)])

    visibilities_0 = plane_0.visibilities_via_transformer_from(
        grid=sub_grid_2d_7x7, transformer=transformer_7x7_7
    )

    visibilities_1 = plane_1.visibilities_via_transformer_from(
        grid=sub_grid_2d_7x7, transformer=transformer_7x7_7
    )

    tracer = al.Tracer(planes=[plane_0, plane_1, plane_2], cosmology=cosmo.Planck15)

    visibilities = tracer.visibilities_list_via_transformer_from(
        grid=sub_grid_2d_7x7, transformer=transformer_7x7_7
    )

    assert (visibilities[0] == visibilities_0).all()
    assert (visibilities[1] == visibilities_1).all()


def test__operate_image__galaxy_blurred_image_2d_dict_via_convolver_from(
    sub_grid_2d_7x7, blurring_grid_2d_7x7, convolver_7x7
):

    g0 = al.Galaxy(redshift=0.5, light_profile=al.lp.EllSersic(intensity=1.0))
    g1 = al.Galaxy(
        redshift=0.5,
        mass_profile=al.mp.SphIsothermal(einstein_radius=1.0),
        light_profile=al.lp.EllSersic(intensity=2.0),
    )

    g2 = al.Galaxy(redshift=0.5, light_profile=al.lp.EllSersic(intensity=3.0))

    g3 = al.Galaxy(redshift=1.0, light_profile=al.lp.EllSersic(intensity=5.0))

    g0_blurred_image = g0.blurred_image_2d_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )

    g1_blurred_image = g1.blurred_image_2d_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )

    g2_blurred_image = g2.blurred_image_2d_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )

    g1_deflections = g1.deflections_yx_2d_from(grid=sub_grid_2d_7x7)

    source_grid_2d_7x7 = sub_grid_2d_7x7 - g1_deflections

    g1_blurring_deflections = g1.deflections_yx_2d_from(grid=blurring_grid_2d_7x7)

    source_blurring_grid_2d_7x7 = blurring_grid_2d_7x7 - g1_blurring_deflections

    g3_blurred_image = g3.blurred_image_2d_via_convolver_from(
        grid=source_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=source_blurring_grid_2d_7x7,
    )

    tracer = al.Tracer.from_galaxies(
        galaxies=[g3, g1, g0, g2], cosmology=cosmo.Planck15
    )

    blurred_image_dict = tracer.galaxy_blurred_image_2d_dict_via_convolver_from(
        grid=sub_grid_2d_7x7,
        convolver=convolver_7x7,
        blurring_grid=blurring_grid_2d_7x7,
    )

    assert (blurred_image_dict[g0].slim == g0_blurred_image.slim).all()
    assert (blurred_image_dict[g1].slim == g1_blurred_image.slim).all()
    assert (blurred_image_dict[g2].slim == g2_blurred_image.slim).all()
    assert (blurred_image_dict[g3].slim == g3_blurred_image.slim).all()


def test__operate_image__galaxy_visibilities_dict_from_grid_and_transformer(
    sub_grid_2d_7x7, transformer_7x7_7
):

    g0 = al.Galaxy(redshift=0.5, light_profile=al.lp.EllSersic(intensity=1.0))
    g1 = al.Galaxy(
        redshift=0.5,
        mass_profile=al.mp.SphIsothermal(einstein_radius=1.0),
        light_profile=al.lp.EllSersic(intensity=2.0),
    )
    g2 = al.Galaxy(redshift=0.5, light_profile=al.lp.EllSersic(intensity=3.0))
    g3 = al.Galaxy(redshift=1.0, light_profile=al.lp.EllSersic(intensity=5.0))

    g0_visibilities = g0.visibilities_via_transformer_from(
        grid=sub_grid_2d_7x7, transformer=transformer_7x7_7
    )
    g1_visibilities = g1.visibilities_via_transformer_from(
        grid=sub_grid_2d_7x7, transformer=transformer_7x7_7
    )

    g2_visibilities = g2.visibilities_via_transformer_from(
        grid=sub_grid_2d_7x7, transformer=transformer_7x7_7
    )

    g1_deflections = g1.deflections_yx_2d_from(grid=sub_grid_2d_7x7)

    source_grid_2d_7x7 = sub_grid_2d_7x7 - g1_deflections

    g3_visibilities = g3.visibilities_via_transformer_from(
        grid=source_grid_2d_7x7, transformer=transformer_7x7_7
    )

    tracer = al.Tracer.from_galaxies(
        galaxies=[g3, g1, g0, g2], cosmology=cosmo.Planck15
    )

    visibilities_dict = tracer.galaxy_visibilities_dict_via_transformer_from(
        grid=sub_grid_2d_7x7, transformer=transformer_7x7_7
    )

    assert (visibilities_dict[g0] == g0_visibilities).all()
    assert (visibilities_dict[g1] == g1_visibilities).all()
    assert (visibilities_dict[g2] == g2_visibilities).all()
    assert (visibilities_dict[g3] == g3_visibilities).all()


def test__operate_lens__sums_individual_quantities():

    grid = al.Grid2D.uniform(shape_native=(50, 50), pixel_scales=0.15)

    sis_0 = al.mp.SphIsothermal(centre=(0.0, 0.0), einstein_radius=0.2)
    sis_1 = al.mp.SphIsothermal(centre=(0.0, 0.0), einstein_radius=0.4)
    sis_2 = al.mp.SphIsothermal(centre=(0.0, 0.0), einstein_radius=0.6)
    sis_3 = al.mp.SphIsothermal(centre=(0.0, 0.0), einstein_radius=0.8)

    galaxy_0 = al.Galaxy(mass_profile_0=sis_0, mass_profile_1=sis_1, redshift=0.5)
    galaxy_1 = al.Galaxy(mass_profile_0=sis_2, mass_profile_1=sis_3, redshift=0.5)

    plane = al.Plane(galaxies=[galaxy_0, galaxy_1])

    tracer = al.Tracer(
        planes=[plane, al.Plane(redshift=1.0, galaxies=None)], cosmology=cosmo.Planck15
    )

    einstein_mass = tracer.einstein_mass_angular_from(grid=grid)

    assert einstein_mass == pytest.approx(np.pi * 2.0 ** 2.0, 1.0e-1)
