# policies/energy_threshold.rego
# OPA policy for energy management in Colossus cluster

package colossus.energy

default allow = false

# Power limit in MW
power_limit_mw := 250

# Minimum Megapack state of charge
min_soc := 0.40

# Allow training if energy constraints are met
allow {
    input.power_mw <= power_limit_mw
    input.megapack_soc >= min_soc
}

# Allow during off-peak hours with relaxed SoC requirement
allow {
    input.power_mw <= power_limit_mw
    input.offpeak == true
}

# Check power consumption
power_check {
    input.power_mw <= power_limit_mw
}

# Check battery state of charge
soc_check {
    input.megapack_soc >= min_soc
}

# Denial reasons
deny[reason] {
    input.power_mw > power_limit_mw
    reason := sprintf("Power consumption %vMW exceeds limit %vMW", [input.power_mw, power_limit_mw])
}

deny[reason] {
    input.megapack_soc < min_soc
    not input.offpeak
    reason := sprintf("Megapack SoC %v below minimum %v (not off-peak)", [input.megapack_soc, min_soc])
}

# Suggested scale factor based on current conditions
suggested_scale = 1.0 {
    input.megapack_soc >= 0.8
    input.power_mw <= power_limit_mw * 0.8
}

suggested_scale = 0.8 {
    input.megapack_soc >= min_soc
    input.megapack_soc < 0.8
    input.power_mw <= power_limit_mw
}

suggested_scale = 0.5 {
    input.megapack_soc < min_soc
}
