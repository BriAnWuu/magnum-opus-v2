"use client";

import Section from "@/components/Section";
import { useMediaQuery, useTheme } from "@mui/material";
import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";

export default function AuctionList() {
  const theme = useTheme();

  const isSm = useMediaQuery(theme.breakpoints.up("sm"));
  const isMd = useMediaQuery(theme.breakpoints.up("md"));
  const isLg = useMediaQuery(theme.breakpoints.up("lg"));
  const isXl = useMediaQuery(theme.breakpoints.up("xl"));

  const imageSize = isXl ? 160 : isLg ? 140 : isMd ? 150 : isSm ? 160 : 100;
  const columns = isXl ? 6 : isLg ? 4 : isMd ? 4 : 2;

  return (
    <Section>
      <ImageList
        sx={{
          position: "relative",
          top: -55,
          width: "100%",
          maxWidth: 1024,
        }}
        variant="quilted"
        cols={columns}
        rowHeight={imageSize}
      >
        {itemData.map((item: ItemData) => (
          <ImageListItem
            key={item.img}
            // cols={item.cols || 1}
            // rows={item.rows || 1}
            cols={item.trending ? 2 : 1}
            rows={item.featured ? 2 : 1}
          >
            <img
              {...srcset(
                item.img,
                imageSize,
                item.trending ? 2 : 1,
                item.featured ? 2 : 1
              )}
              alt={item.title}
              loading="lazy"
            />
          </ImageListItem>
        ))}
      </ImageList>
    </Section>
  );
}

const srcset = (image: string, size: number, cols = 1, rows = 1) => {
  return {
    src: `${image}?w=${size * cols}&h=${size * rows}&fit=crop&auto=format`,
    srcSet: `${image}?w=${size * cols}&h=${
      size * rows
    }&fit=crop&auto=format&dpr=2 2x`,
  };
};

interface ItemData {
  img: string;
  title: string;
  trending: boolean; // High click-through rate
  featured: boolean; // High click-through and bid rate
  author?: string;
}

const itemData: ItemData[] = [
  {
    img: "https://images.unsplash.com/photo-1551963831-b3b1ca40c98e",
    title: "Breakfast",
    // rows: 2,
    // cols: 2,
    trending: true,
    featured: true,
  },
  {
    img: "https://images.unsplash.com/photo-1551782450-a2132b4ba21d",
    title: "Burger",
    trending: false,
    featured: false,
  },
  {
    img: "https://images.unsplash.com/photo-1522770179533-24471fcdba45",
    title: "Camera",
    trending: false,
    featured: false,
  },
  {
    img: "https://images.unsplash.com/photo-1444418776041-9c7e33cc5a9c",
    title: "Coffee",
    // cols: 2,
    trending: true,
    featured: false,
  },
  {
    img: "https://images.unsplash.com/photo-1533827432537-70133748f5c8",
    title: "Hats",
    // cols: 2,
    trending: true,
    featured: false,
  },
  {
    img: "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62",
    title: "Honey",
    author: "@arwinneil",
    // rows: 2,
    // cols: 2,
    trending: true,
    featured: true,
  },
  {
    img: "https://images.unsplash.com/photo-1516802273409-68526ee1bdd6",
    title: "Basketball",
    trending: false,
    featured: false,
  },
  {
    img: "https://images.unsplash.com/photo-1518756131217-31eb79b20e8f",
    title: "Fern",
    trending: false,
    featured: false,
  },
  {
    img: "https://images.unsplash.com/photo-1597645587822-e99fa5d45d25",
    title: "Mushrooms",
    // rows: 2,
    // cols: 2,
    trending: true,
    featured: true,
  },
  {
    img: "https://images.unsplash.com/photo-1567306301408-9b74779a11af",
    title: "Tomato basil",
    trending: false,
    featured: false,
  },
  {
    img: "https://images.unsplash.com/photo-1471357674240-e1a485acb3e1",
    title: "Sea star",
    trending: false,
    featured: false,
  },
  {
    img: "https://images.unsplash.com/photo-1589118949245-7d38baf380d6",
    title: "Bike",
    // cols: 2,
    trending: true,
    featured: false,
  },
];
