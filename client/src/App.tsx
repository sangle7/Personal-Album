import React, { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

import Box from '@mui/material/Box';
import TitlebarImageList from './ImageList';
import useStyles from './styles';

interface Props {}

const ExampleComponent: React.FC<Props> = () => {
  const classes = useStyles();
  const [query, setQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [images, setImages] = useState<string[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://127.0.0.1:5000/search');
      const json = await response.json();
      setImages(json);
    };

    console.log('run!')

    fetchData();
  }, []);

  const fetchImages = async () => {
    setLoading(true);
    const response = await fetch(`http://127.0.0.1:5000/search?query=${query}`);
    const responseJson = await response.json();
    setLoading(false);
    setImages(responseJson);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') fetchImages();
  };

  return (
    <div className={classes.container}>
      <Box
        sx={{
          '& > :not(style)': { m: 1, width: '25ch' },
        }}
      >
        <TextField
          id='outlined-basic'
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          label='Search Images By Text'
          variant='outlined'
        />
        <Button variant='contained' onClick={fetchImages}>
          Submit
        </Button>
      </Box>
      {loading ? (
        <div className={classes.loader}></div>
      ) : (
        <TitlebarImageList itemData={images} />
      )}
    </div>
  );
};

export default ExampleComponent;
