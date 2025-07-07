import taxbrain.utils
import pytest


def test_distribution_plot(tb_static_run):
    fig = taxbrain.utils.distribution_plot(tb_static_run, 2019)
    assert fig is not None


def test_differences_plot(tb_static_run):
    fig = taxbrain.utils.differences_plot(tb_static_run, "combined")
    assert fig is not None
    with pytest.raises(AssertionError):
        taxbrain.utils.differences_plot(tb_static_run, "wages")


def test_volcano_plot(tb_static_run):
    fig = taxbrain.utils.volcano_plot(tb_static_run, 2019)
    assert fig is not None
    with pytest.raises(ValueError):
        taxbrain.utils.volcano_plot(tb_static_run, 2019, min_y=-10000)
    fig = taxbrain.utils.volcano_plot(tb_static_run, 2019, min_y=-1000, log_scale=False)
    # testing using RGB tuples for the colors
    fig = taxbrain.utils.volcano_plot(
        tb_static_run,
        2019,
        increase_color=(0.1, 0.2, 0.5),
        decrease_color=(0.2, 0.2, 0.5),
    )


def test_lorenz_curve(tb_static_run):
    fig = taxbrain.utils.lorenz_curve(tb_static_run, 2019)
    assert fig is not None


def test_revenue_plot(tb_static_run):
    fig = taxbrain.utils.revenue_plot(tb_static_run)
    assert fig is not None
    with pytest.raises(ValueError):
        taxbrain.utils.revenue_plot(tb_static_run, tax_vars=["income", "combined"])
    with pytest.raises(AssertionError):
        taxbrain.utils.revenue_plot(tb_static_run, tax_vars=[])
