from pricing import add_gst, delivery_fee, loyalty_points, member_price


def test_member_price_normal_discount():
    assert member_price(1000, 10) == 900
    assert member_price(750, 20) == 600


def test_member_price_zero_discount():
    assert member_price(250, 0) == 250


def test_member_price_full_discount():
    assert member_price(250, 100) == 0


def test_add_gst_default_and_custom_rate():
    assert add_gst(1000) == 1050
    assert add_gst(1000, 12) == 1120


def test_delivery_fee_normal_cases():
    assert delivery_fee(300) == 40
    assert delivery_fee(600) == 0


def test_delivery_fee_threshold_boundary():
    assert delivery_fee(499) == 40
    assert delivery_fee(500) == 0


def test_loyalty_points_normal_and_edge_cases():
    assert loyalty_points(950) == 9
    assert loyalty_points(100) == 1
    assert loyalty_points(99) == 0
