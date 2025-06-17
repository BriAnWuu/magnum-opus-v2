import { Box, Typography } from "@mui/material";

export default function ExampleTypography() {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: { xs: "column", md: "row" },
        justifyContent: "center",
        alignItems: "center",
        gap: 1,
        padding: 1,
      }}
    >
      <Typography variant="h1" color="primary">
        Hello
      </Typography>
      <Typography variant="h2" color="secondary">
        Welcome to Material UI
      </Typography>
      <Typography variant="h3" color="text.primary">
        Explore the features of our application
      </Typography>
      <Typography variant="subtitle1" color="text.secondary">
        This is a subtitle with secondary text color
      </Typography>
      <Typography variant="body1" color="info">
        This is a sample application built with Material UI and Next.js. You can
        toggle between light and dark modes using the button below.
      </Typography>
      <Typography variant="body2" color="success">
        Enjoy the flexibility and customization options that Material UI
        provides.
      </Typography>
      <Typography variant="body2" color="warning">
        Don't forget to check the documentation for more details.
      </Typography>
      <Typography variant="body2" color="error">
        If you encounter any issues, please reach out for support.
      </Typography>
    </Box>
  );
}
