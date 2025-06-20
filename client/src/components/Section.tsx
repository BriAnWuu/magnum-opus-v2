import { Box } from "@mui/material";

export default function Section({ children }: { children: React.ReactNode }) {
  return (
    <Box
      component="section"
      sx={{
        display: "flex",
        justifyContent: "center",
        paddingX: { xs: 2, lg: 4 },
      }}
    >
      {children}
    </Box>
  );
}
