#!/usr/bin/env python3
"""
Ocean Clock - A minimalist Tkinter desktop clock.

This application displays the current time in a modern UI using the Ocean Professional theme:
- primary: #2563EB
- secondary: #F59E0B
- background: #f9fafb
- surface: #ffffff
- text: #111827

Security and quality:
- PEP 8 compliance
- Avoids blocking loops (uses Tkinter's after scheduler)
- Graceful shutdown handling
- No external dependencies
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from typing import Optional
import tkinter as tk
from tkinter import ttk


@dataclass(frozen=True)
class Theme:
    """Theme colors for the Ocean Professional look."""
    primary: str = "#2563EB"
    secondary: str = "#F59E0B"
    background: str = "#f9fafb"
    surface: str = "#ffffff"
    text: str = "#111827"


class OceanClockApp:
    """
    OceanClockApp encapsulates the Tkinter UI and update loop.

    It sets a modern, minimalist UI with a large time display and an accent underline.
    """

    def __init__(self, root: tk.Tk, theme: Optional[Theme] = None) -> None:
        self.root = root
        self.theme = theme or Theme()

        # Keep track of scheduled after() call so we can cancel on shutdown.
        self._update_job: Optional[str] = None

        self._configure_root()
        self._build_ui()
        self._bind_events()

    def _configure_root(self) -> None:
        """Configure application window and overall background."""
        self.root.title("Ocean Clock")
        # Minimal window size to keep layout tidy
        self.root.minsize(360, 220)
        # Set app background
        self.root.configure(bg=self.theme.background)

        # On some platforms, ttk inherits the native theme; set default to 'clam' for consistency
        try:
            style = ttk.Style()
            # Ensure a theme that supports custom styling
            style.theme_use("clam")
        except tk.TclError:
            # If theme is unavailable, ignore and proceed with defaults
            pass

    def _build_ui(self) -> None:
        """
        Build the main UI:
        - Centered container with rounded-like effect and subtle shadow illusion
        - Large time label
        - Accent underline using secondary color
        """
        # Outer frame to create spacing from window edges (background gradient imitation)
        self.outer = tk.Frame(self.root, bg=self.theme.background, highlightthickness=0, bd=0)
        self.outer.pack(fill="both", expand=True, padx=16, pady=16)

        # Surface container (rounded look simulated with padding, border-radius is not native in Tk)
        self.container = tk.Frame(
            self.outer,
            bg=self.theme.surface,
            highlightbackground=self.theme.primary,
            highlightthickness=0,
            bd=0,
            relief="flat",
        )
        # Center the container
        self.container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.72)

        # Create a subtle shadow effect using another frame behind the container
        self.shadow = tk.Frame(self.outer, bg="#e5e7eb", bd=0, highlightthickness=0)
        # Place behind container (lower z-order)
        self.shadow.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92, relheight=0.72, y=6)
        self.shadow.lower(self.container)

        # Time label
        self.time_var = tk.StringVar(value="--:--:--")
        self.time_label = tk.Label(
            self.container,
            textvariable=self.time_var,
            font=("Segoe UI", 56, "bold"),
            fg=self.theme.text,
            bg=self.theme.surface,
        )
        self.time_label.pack(padx=24, pady=(28, 8))

        # Accent underline (secondary color)
        self.accent = tk.Frame(self.container, bg=self.theme.secondary, height=4, bd=0, highlightthickness=0)
        self.accent.pack(fill="x", padx=64, pady=(0, 24))

        # Subtle helper text using primary color
        self.sub_text = tk.Label(
            self.container,
            text="Ocean Professional",
            font=("Segoe UI", 10),
            fg=self.theme.primary,
            bg=self.theme.surface,
        )
        self.sub_text.pack(pady=(0, 16))

        # Adjust font responsively
        self._resize_fonts()

        # Begin the update loop
        self._schedule_update()

    def _bind_events(self) -> None:
        """Bind window events for resize and graceful shutdown."""
        self.root.bind("<Configure>", self._on_resize)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_resize(self, event: tk.Event) -> None:
        """Handle window resize to adjust font sizes responsively."""
        # Avoid using event in ways that may not exist on all platforms
        try:
            width = max(self.root.winfo_width(), 1)
            height = max(self.root.winfo_height(), 1)
        except tk.TclError:
            return

        # Recompute fonts based on size
        self._resize_fonts(width, height)

    def _resize_fonts(self, width: Optional[int] = None, height: Optional[int] = None) -> None:
        """Resize main time font proportionally to window size."""
        try:
            width = width or self.root.winfo_width()
            height = height or self.root.winfo_height()
        except tk.TclError:
            return

        # Heuristic for font size based on the smaller dimension
        base = max(min(int(min(width, height) * 0.18), 120), 28)
        self.time_label.configure(font=("Segoe UI", base, "bold"))

    def _schedule_update(self) -> None:
        """Schedule the periodic time update using Tkinter's after method."""
        # Update every 200 ms for smoothness
        self._update_job = self.root.after(200, self._update_time)

    def _update_time(self) -> None:
        """Update the displayed time and reschedule the update."""
        # Use time.strftime for locale-agnostic time format HH:MM:SS
        now = time.strftime("%H:%M:%S")
        self.time_var.set(now)
        self._schedule_update()

    def _cancel_update(self) -> None:
        """Cancel any scheduled update callback to ensure clean shutdown."""
        if self._update_job is not None:
            try:
                self.root.after_cancel(self._update_job)
            except tk.TclError:
                # If already cancelled or root is destroyed, ignore
                pass
            finally:
                self._update_job = None

    def _on_close(self) -> None:
        """Handle window close: cancel updates and destroy the root safely."""
        self._cancel_update()
        try:
            self.root.destroy()
        except tk.TclError:
            # If already destroyed or destroying, ignore
            pass


# PUBLIC_INTERFACE
def main() -> int:
    """
    Application entry point.

    Initializes the Tk root, constructs the OceanClockApp, and starts the main loop.

    Returns:
        int: Process exit code (0 on normal exit).
    """
    try:
        root = tk.Tk()
    except tk.TclError:
        # If Tk cannot initialize (e.g., no DISPLAY), exit gracefully with non-zero code.
        return 1

    app = OceanClockApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        # Allow Ctrl+C to close gracefully
        app._on_close()  # noqa: SLF001 - internal cleanup on exit
    return 0


if __name__ == "__main__":
    sys.exit(main())
