"""
Pydantic models for the Life Planning Coach conversation state.

Defines LifeWheel, Values, Goals, WOOP, WeeklyReview, and ConversationState
based on the JSON schema from SKILL.md.
"""

from __future__ import annotations

import json
from datetime import date
from typing import Any

from pydantic import BaseModel, Field, field_validator


class LifeWheel(BaseModel):
    """8-sphere Wheel of Life assessment (1–10 scale)."""

    health: int = Field(default=5, ge=1, le=10)
    career: int = Field(default=5, ge=1, le=10)
    finances: int = Field(default=5, ge=1, le=10)
    relationships: int = Field(default=5, ge=1, le=10)
    personal_growth: int = Field(default=5, ge=1, le=10)
    fun_recreation: int = Field(default=5, ge=1, le=10)
    physical_environment: int = Field(default=5, ge=1, le=10)
    family_friends: int = Field(default=5, ge=1, le=10)


class Values(BaseModel):
    """Schwartz Portrait Value Questionnaire (PVQ) scores (0.0–1.0)."""

    power: float = 0.5
    achievement: float = 0.5
    hedonism: float = 0.5
    stimulation: float = 0.5
    self_direction: float = 0.5
    universalism: float = 0.5
    benevolence: float = 0.5
    tradition: float = 0.5
    conformity: float = 0.5
    security: float = 0.5


class OKRTheme(BaseModel):
    """A single life-theme OKR (1–3 year horizon)."""

    objective: str = ""
    key_results: list[str] = Field(default_factory=list)


class TwelveWeek(BaseModel):
    """12-Week Year OKR structure."""

    objectives: list[str] = Field(default_factory=list)
    key_results: list[str] = Field(default_factory=list)


class WOOP(BaseModel):
    """Wish-Outcome-Obstacle-Plan implementation intention."""

    wish: str = ""
    outcome: str = ""
    obstacle: str = ""
    plan: str = ""


class Goals(BaseModel):
    """Multi-layer goal architecture."""

    bhag: str = ""
    themes: list[OKRTheme] = Field(default_factory=list)
    twelve_week: TwelveWeek = Field(default_factory=TwelveWeek)
    weekly: list[str] = Field(default_factory=list)
    daily_woop: list[WOOP] = Field(default_factory=list)


class WeeklyReview(BaseModel):
    """GTD + Scrum retrospective weekly review entry."""

    date: str = ""
    format: str = "gtd_scrum"
    worked: list[str] = Field(default_factory=list)
    didnt_work: list[str] = Field(default_factory=list)
    changes: list[str] = Field(default_factory=list)
    lead_measures: dict[str, Any] = Field(default_factory=dict)
    lag_measures: dict[str, Any] = Field(default_factory=dict)
    adjustments: list[str] = Field(default_factory=list)


class ConversationState(BaseModel):
    """Full conversation state for checkpoint-and-resume."""

    user_id: str = ""
    stage: int = 1
    phase: str = ""
    completed_phases: list[str] = Field(default_factory=list)
    current_question: int = 0
    life_wheel: LifeWheel = Field(default_factory=LifeWheel)
    values: Values = Field(default_factory=Values)
    goals: Goals = Field(default_factory=Goals)
    weekly_reviews: list[WeeklyReview] = Field(default_factory=list)

    @field_validator("stage")
    @classmethod
    def _validate_stage(cls, v: int) -> int:
        if v not in (1, 2, 3):
            raise ValueError(f"stage must be 1, 2, or 3, got {v}")
        return v

    @field_validator("life_wheel")
    @classmethod
    def _validate_life_wheel(cls, v: LifeWheel) -> LifeWheel:
        for field_name in LifeWheel.model_fields:
            score = getattr(v, field_name)
            if not 1 <= score <= 10:
                raise ValueError(
                    f"life_wheel.{field_name} must be between 1 and 10, got {score}"
                )
        return v

    # --- serialization helpers ---

    def to_json(self) -> str:
        """Serialize state to a JSON string."""
        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, raw: str) -> "ConversationState":
        """Deserialize state from a JSON string."""
        return cls.model_validate_json(raw)

    def export_markdown(self) -> str:
        """Export state as a human-readable Markdown document."""
        lines: list[str] = []
        lines.append("# Life Planning Coach — Session Report\n")
        lines.append(f"- **User ID**: {self.user_id}")
        lines.append(f"- **Stage**: {self.stage}")
        lines.append(f"- **Phase**: {self.phase}")
        lines.append(f"- **Current Question**: {self.current_question}")
        lines.append(f"- **Completed Phases**: {', '.join(self.completed_phases) or '—'}\n")

        lines.append("## Wheel of Life\n")
        for field_name in LifeWheel.model_fields:
            label = field_name.replace("_", " ").title()
            lines.append(f"- **{label}**: {getattr(self.life_wheel, field_name)}/10")
        lines.append("")

        lines.append("## Values (Schwartz PVQ)\n")
        for field_name in Values.model_fields:
            label = field_name.replace("_", " ").title()
            lines.append(f"- **{label}**: {getattr(self.values, field_name):.2f}")
        lines.append("")

        lines.append("## Goals\n")
        lines.append(f"### BHAG\n{self.goals.bhag or '—'}\n")

        if self.goals.themes:
            lines.append("### Life Themes")
            for i, theme in enumerate(self.goals.themes, start=1):
                lines.append(f"{i}. **{theme.objective}**")
                for kr in theme.key_results:
                    lines.append(f"   - {kr}")
            lines.append("")

        if self.goals.twelve_week.objectives or self.goals.twelve_week.key_results:
            lines.append("### 12-Week Quarter")
            lines.append("**Objectives:**")
            for obj in self.goals.twelve_week.objectives:
                lines.append(f"- {obj}")
            lines.append("**Key Results:**")
            for kr in self.goals.twelve_week.key_results:
                lines.append(f"- {kr}")
            lines.append("")

        if self.goals.weekly:
            lines.append("### Weekly Priorities")
            for item in self.goals.weekly:
                lines.append(f"- {item}")
            lines.append("")

        if self.goals.daily_woop:
            lines.append("### Daily WOOP")
            for w in self.goals.daily_woop:
                lines.append(f"- **Wish**: {w.wish}")
                lines.append(f"  **Outcome**: {w.outcome}")
                lines.append(f"  **Obstacle**: {w.obstacle}")
                lines.append(f"  **Plan**: {w.plan}")
            lines.append("")

        if self.weekly_reviews:
            lines.append("## Weekly Reviews\n")
            for review in self.weekly_reviews:
                lines.append(f"### {review.date} ({review.format})")
                lines.append("**Worked:**")
                for item in review.worked:
                    lines.append(f"- {item}")
                lines.append("**Didn't Work:**")
                for item in review.didnt_work:
                    lines.append(f"- {item}")
                lines.append("**Changes:**")
                for item in review.changes:
                    lines.append(f"- {item}")
                lines.append("")

        return "\n".join(lines)
