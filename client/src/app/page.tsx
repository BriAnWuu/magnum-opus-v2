"use client";

import ExampleTypography from "@/components/ExampleTypography";
import { useTheme } from "@mui/material";
import Box from "@mui/material/Box";

export default function Home() {
  const theme = useTheme();
  const drawerWidth =
    (theme.components?.MuiDrawer?.styleOverrides?.paper as { width?: number })
      ?.width || 250;

  return (
    <Box
      component="main"
      sx={{
        flexGrow: 1,
        width: {
          xs: "50%",
          lg: `calc(100% - ${drawerWidth}px)`,
        },
      }}
    >
      <ExampleTypography />
    </Box>
  );
}
