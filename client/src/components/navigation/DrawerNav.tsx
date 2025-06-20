"use client";

import DarkModeToggle from "@/components/navigation/DarkModeToggle";
import FilterVintageIcon from "@mui/icons-material/FilterVintage";
import MenuIcon from "@mui/icons-material/Menu";
import {
  alpha,
  Box,
  Divider,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
} from "@mui/material";
import { useState } from "react";

const navList = [
  { text: "Home", href: "/" },
  { text: "About", href: "/about" },
  { text: "Services", href: "/services" },
  { text: "Contact", href: "/contact" },
];

const userManagementList = [
  { text: "Sign In", href: "/signin" },
  { text: "Profile", href: "/profile" },
  { text: "Settings", href: "/settings" },
];

export default function DrawerNav() {
  const [open, setOpen] = useState(false);
  const toggleDrawer = (newOpen: boolean) => {
    setOpen(newOpen);
  };

  const DrawerContent = (
    <Box
      sx={{ display: "flex", flexDirection: "column", height: "100%" }}
      onClick={() => toggleDrawer(false)}
    >
      <IconButton sx={{ margin: 1, alignSelf: "flex-start" }}>
        <FilterVintageIcon />
      </IconButton>
      <List>
        {navList.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton>
              <ListItemText>
                <Typography variant="h5" color="text.primary">
                  {item.text}
                </Typography>
              </ListItemText>
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        {userManagementList.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton>
              <ListItemText>
                <Typography variant="h5" color="text.primary">
                  {item.text}
                </Typography>
              </ListItemText>
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <DarkModeToggle
        sx={{ margin: 2, marginTop: "auto", alignSelf: "flex-end" }}
      />
    </Box>
  );

  return (
    <Box component="nav" sx={{ flexShrink: { xs: 0 } }} aria-label="navigation">
      {/* mobile view */}
      <IconButton
        sx={{
          position: "fixed",
          top: 8,
          left: 8,
          backgroundColor: alpha("#FFF", 0.25),
          zIndex: 999,
          display: { xs: "flex", lg: "none" },
        }}
        onClick={() => toggleDrawer(true)}
      >
        <MenuIcon />
      </IconButton>
      <Drawer
        variant="temporary"
        anchor="left"
        open={open}
        onClose={() => toggleDrawer(false)}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          display: { xs: "block", lg: "none" },
        }}
      >
        {DrawerContent}
      </Drawer>

      {/* laptop view */}
      <Drawer
        variant="permanent"
        anchor="left"
        open
        sx={{
          display: { xs: "none", lg: "block" },
        }}
      >
        {DrawerContent}
      </Drawer>
    </Box>
  );
}
