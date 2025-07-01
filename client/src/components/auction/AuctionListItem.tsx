import { ItemData } from "@/components/auction/AuctionList";
import InfoIcon from "@mui/icons-material/Info";
import { IconButton, ImageListItem, ImageListItemBar } from "@mui/material";
import { useState } from "react";

export default function AuctionListItem({
  img,
  title,
  trending,
  featured,
  author,
  imageSize,
}: ItemData & { imageSize: number }) {
  const [hovered, setHovered] = useState(false);

  return (
    <ImageListItem
      // cols={item.cols || 1}
      // rows={item.rows || 1}
      cols={trending ? 2 : 1}
      rows={featured ? 2 : 1}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <img
        {...srcset(img, imageSize, trending ? 2 : 1, featured ? 2 : 1)}
        alt={title}
        loading="lazy"
      />
      {hovered && (
        <ImageListItemBar
          title={title}
          subtitle={author}
          position="bottom"
          actionIcon={
            <IconButton
              sx={{ color: "rgba(255, 255, 255, 0.5)" }}
              aria-label={`info about ${title}`}
            >
              <InfoIcon />
            </IconButton>
          }
        />
      )}
    </ImageListItem>
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
