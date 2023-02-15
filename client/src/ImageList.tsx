import * as React from 'react';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import ListSubheader from '@mui/material/ListSubheader';

interface Props {
  itemData: any;
}

const TitlebarImageList: React.FC<Props> = ({ itemData = [] }) => {
  return (
    <ImageList sx={{ width: 800 }} variant="masonry" cols={3} gap={8}>
      {itemData.map((item) => (
        <ImageListItem key={item.img}>
          <img src={`http://localhost:5000/${item.FileName}`} alt={item.FileName} loading='lazy' />
          <ImageListItemBar title={item.FileName} subtitle={item.similarity}/>
        </ImageListItem>
      ))}
    </ImageList>
  );
};

export default TitlebarImageList;
