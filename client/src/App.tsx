import React, { useEffect, useState } from 'react';
import useStyles from './styles';

interface Props {}

const ExampleComponent: React.FC<Props> = () => {
  const classes = useStyles();
  const [query, setQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [images, setImages] = useState<string[]>([]);

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
      <h1 className={classes.root}>Search Images By Text</h1>
      <input
        type='text'
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button onClick={fetchImages}> Submit </button>
      <div className={classes.imageGallery}>
        {loading ? (
          <div className={classes.loader}></div>
        ) : (
          images &&
          images.map((image, index) => (
            <div className={classes.singleImageContainer}>
              <img
                height='300'
                key={index}
                src={`http://127.0.0.1:5000/${image['FileName']}`}
              />
              <p>similarity: {image['similarity']}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ExampleComponent;
