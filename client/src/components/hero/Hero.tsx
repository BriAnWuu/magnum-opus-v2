import { Box, Typography } from "@mui/material";

export default function Hero() {
  return (
    <Box
      component="header"
      sx={{
        bgcolor: "primary.main",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: 2,
        paddingBottom: 8,
      }}
    >
      <Typography variant="h1" color="text.primary">
        Mag Example
      </Typography>
    </Box>
  );
}
