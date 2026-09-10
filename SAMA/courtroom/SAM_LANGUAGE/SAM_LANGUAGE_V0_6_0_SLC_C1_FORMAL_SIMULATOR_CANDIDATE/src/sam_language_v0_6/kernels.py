"""Scientific calculation kernels available to SAM Language v0.5.0."""

from __future__ import annotations

import math


def earth_orbit_clock_packet(
    *,
    speed_of_light_m_s: float,
    earth_mu_m3_s2: float,
    earth_ground_radius_m: float,
    orbit_radius_m: float,
    nominal_clock_frequency_hz: float,
    seconds_per_day: float,
) -> dict[str, float]:
    """Run the CR005 circular Earth-orbit clock calculation unchanged."""

    c = speed_of_light_m_s
    mu = earth_mu_m3_s2
    r_ground = earth_ground_radius_m
    r_orbit = orbit_radius_m
    nominal = nominal_clock_frequency_hz
    day = seconds_per_day

    values = (c, mu, r_ground, r_orbit, nominal, day)
    if any(value <= 0.0 for value in values):
        raise ValueError("Earth-orbit clock inputs must all be positive")

    A_ground = 2.0 * mu / (c * c * r_ground)
    A_orbit = 2.0 * mu / (c * c * r_orbit)
    v_orbit = math.sqrt(mu / r_orbit)

    gravity_exact = math.sqrt(1.0 - A_orbit) / math.sqrt(1.0 - A_ground) - 1.0
    gravity_weak = (A_ground - A_orbit) / 2.0

    sr_exact = math.sqrt(1.0 - (v_orbit * v_orbit) / (c * c)) - 1.0
    sr_weak = -(v_orbit * v_orbit) / (2.0 * c * c)

    net_exact = gravity_exact + sr_exact
    net_weak = gravity_weak + sr_weak
    factory = nominal * (1.0 - net_exact)

    return {
        "speed_of_light_m_s": c,
        "earth_mu_m3_s2": mu,
        "earth_ground_radius_m": r_ground,
        "orbit_radius_m": r_orbit,
        "nominal_clock_frequency_hz": nominal,
        "seconds_per_day": day,
        "A_ground": A_ground,
        "A_orbit": A_orbit,
        "orbit_speed_m_s": v_orbit,
        "gravity_exact_us_day": gravity_exact * day * 1e6,
        "gravity_weak_us_day": gravity_weak * day * 1e6,
        "sr_exact_us_day": sr_exact * day * 1e6,
        "sr_weak_us_day": sr_weak * day * 1e6,
        "net_exact_us_day": net_exact * day * 1e6,
        "net_weak_us_day": net_weak * day * 1e6,
        "factory_frequency_hz": factory,
    }
