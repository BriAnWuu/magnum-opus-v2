"use client";

import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import { ToggleButton, useColorScheme } from "@mui/material";

interface DarkModeToggleProps {
  sx: React.CSSProperties;
}

export default function DarkModeToggle({ sx }: DarkModeToggleProps) {
  const { setMode, mode } = useColorScheme();

  const handleToggle = () => {
    if (mode === "system") {
      setMode("dark");
    } else if (mode === "dark") {
      setMode("light");
    } else {
      setMode("system");
    }
  };

  const icon =
    mode === "dark" ? <LightModeOutlinedIcon /> : <DarkModeOutlinedIcon />;

  const tooltipText =
    mode === "system"
      ? "Switch to Dark Mode"
      : mode === "dark"
      ? "Switch to Light Mode"
      : "Switch to System Mode";

  return (
    <ToggleButton
      value="darkModeToggle"
      onClick={handleToggle}
      title={tooltipText}
      aria-label={tooltipText}
      sx={sx}
    >
      {icon}
    </ToggleButton>
  );
}
