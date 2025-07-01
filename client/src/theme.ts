"use client";

import { amber, grey, lightGreen, red } from "@mui/material/colors";
import { createTheme, responsiveFontSizes } from "@mui/material/styles";
import { Roboto } from "next/font/google";

const roboto = Roboto({
  weight: ["300", "400", "500", "600"],
  style: ["normal", "italic"],
  subsets: ["latin"],
  display: "swap",
  variable: "--font-roboto",
  fallback: ["system-ui", "arial"],
});

const theme = createTheme({
  colorSchemes: {
    light: {
      palette: {
        primary: {
          main: "#B17457",
        },
        secondary: {
          main: "#D8D2C2",
        },
        error: { main: red[500] },
        warning: { main: amber[300] },
        info: { main: grey[800] },
        success: { main: lightGreen["A400"] },
        background: { default: "#FAF7F0", paper: "#F4EDDD" },
        text: { primary: "#4A4947" },
      },
    },
    dark: {
      palette: {
        primary: {
          main: "#B17457",
        },
        secondary: {
          main: "#D8D2C2",
        },
        error: { main: red[500] },
        warning: { main: amber[300] },
        info: { main: grey[300] },
        success: { main: lightGreen["A400"] },
        background: { default: "#4A4947", paper: "#5C5B59" },
        text: { primary: "#FAF7F0" },
      },
    },
  },
  cssVariables: {
    colorSchemeSelector: "class",
  },
  typography: {
    fontFamily: roboto.style.fontFamily,
    h1: { fontSize: "4rem", lineHeight: 1.167 },
    h2: { fontSize: "2.375rem", lineHeight: 1.2 },
    h3: { fontSize: "2rem", lineHeight: 1.167 },
    h4: { fontSize: "1.6rem", lineHeight: 1.235 },
    h5: { fontSize: "1.25rem", lineHeight: 1.334 },
    h6: { fontSize: "1.125rem", lineHeight: 1.6 },
    subtitle1: { fontSize: "1rem", lineHeight: 1.75 },
    subtitle2: { fontSize: "1rem", lineHeight: 1.57 },
    body1: { fontSize: "0.875rem", lineHeight: 1.5 },
    body2: { fontSize: "0.875rem", lineHeight: 1.5, fontWeight: 600 },
    button: { fontSize: "0.75rem", lineHeight: 1.75 },
    caption: { fontSize: "0.75rem", lineHeight: 1.667 },
    overline: { fontSize: "0.75rem", lineHeight: 2.667 },
  },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 768,
      lg: 1024,
      xl: 1280,
    },
  },
  shape: { borderRadius: 8 },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          width: 250,
          boxSizing: "border-box",
          borderRadius: 0,
          borderStartEndRadius: 8,
          borderEndEndRadius: 8,
        },
      },
    },
    MuiImageListItem: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          overflow: "hidden",
          cursor: "pointer",
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
  },
});

export default responsiveFontSizes(theme);
