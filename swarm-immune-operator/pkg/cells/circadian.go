// Package cells provides cell type implementations for the immune system
package cells

import (
	"time"
)

// CircadianCalculator calculates scaling based on time of day
// This mimics the body's natural rhythm of activity and rest
type CircadianCalculator struct {
	SunriseHour int // Hour when sunshine mode begins (e.g., 6 for 6:00 AM)
	SunsetHour  int // Hour when moonlight mode begins (e.g., 22 for 10:00 PM)
}

// Mode represents the current circadian mode
type Mode string

const (
	// ModeSunshine represents active/daytime mode with higher scaling
	ModeSunshine Mode = "sunshine"
	// ModeMoonlight represents sleep/nighttime mode with lower scaling
	ModeMoonlight Mode = "moonlight"
)

// NewCircadianCalculator creates a new calculator with default hours
func NewCircadianCalculator() *CircadianCalculator {
	return &CircadianCalculator{
		SunriseHour: 6,
		SunsetHour:  22,
	}
}

// CurrentMode returns the current circadian mode based on the current time
func (c *CircadianCalculator) CurrentMode() Mode {
	return c.ModeAt(time.Now())
}

// ModeAt returns the circadian mode at a specific time
func (c *CircadianCalculator) ModeAt(t time.Time) Mode {
	hour := t.Hour()
	if hour >= c.SunriseHour && hour < c.SunsetHour {
		return ModeSunshine
	}
	return ModeMoonlight
}

// GetTargetReplicas returns the appropriate replica count based on mode
func (c *CircadianCalculator) GetTargetReplicas(sunshineReplicas, moonlightReplicas int32) int32 {
	if c.CurrentMode() == ModeSunshine {
		return sunshineReplicas
	}
	return moonlightReplicas
}

// GetTargetReplicasAt returns replicas for a specific time
func (c *CircadianCalculator) GetTargetReplicasAt(t time.Time, sunshineReplicas, moonlightReplicas int32) int32 {
	if c.ModeAt(t) == ModeSunshine {
		return sunshineReplicas
	}
	return moonlightReplicas
}

// TimeUntilModeChange returns the duration until the next mode change
func (c *CircadianCalculator) TimeUntilModeChange() time.Duration {
	now := time.Now()
	currentHour := now.Hour()

	var targetHour int
	if c.CurrentMode() == ModeSunshine {
		targetHour = c.SunsetHour
	} else {
		targetHour = c.SunriseHour
		if currentHour >= c.SunsetHour {
			// After sunset, sunrise is tomorrow
			targetHour += 24
		}
	}

	hoursUntil := targetHour - currentHour
	targetTime := time.Date(now.Year(), now.Month(), now.Day(), now.Hour()+hoursUntil, 0, 0, 0, now.Location())

	return targetTime.Sub(now)
}

// IsSunshine returns true if currently in sunshine mode
func (c *CircadianCalculator) IsSunshine() bool {
	return c.CurrentMode() == ModeSunshine
}

// IsMoonlight returns true if currently in moonlight mode
func (c *CircadianCalculator) IsMoonlight() bool {
	return c.CurrentMode() == ModeMoonlight
}
