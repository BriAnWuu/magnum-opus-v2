"use client";

import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    colorSchemes: {
        light: {
            palette: {
                primary: {
                    main: "",
                    light: "",
                    dark: "",
                },
                secondary: {
                    main: "",
                    light: "",
                    dark: "",
                },
                error: {
                    main: "",
                },
                warning: { main: "" },
                info: { main: "" },
                success: { main: "" },
            },
        },
        dark: {
            palette: {
                primary: {
                    main: "",
                    light: "",
                    dark: "",
                },
                secondary: {
                    main: "",
                    light: "",
                    dark: "",
                },
                error: {
                    main: "",
                },
                warning: { main: "" },
                info: { main: "" },
                success: { main: "" },
            },
        },
    },
    cssVariables: {
        colorSchemeSelector: "class",
    },
    typography: {
        fontFamily: "var(--font-roboto)",
        h1: {},
        h2: {},
        h3: {},
        h4: {},
        h5: {},
        h6: {},
        subtitle1: {},
        subtitle2: {},
        body1: {},
        body2: {},
        button: {},
        caption: {},
        overline: {},
    },
    breakpoints: {
        values: {
            xs: 0,
            sm: 320,
            md: 768,
            lg: 1280,
            xl: 1440,
        },
    },
    components: {},
});

export default theme;
