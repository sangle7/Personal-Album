import { createUseStyles } from 'react-jss'

const useStyles = createUseStyles({
  '@keyframes spin': {
    '0%': { transform: 'rotate(0deg)' },
    '50%': { transform: 'rotate(180deg)' },
    '100%': { transform: 'rotate(360deg)' },
  },
  root: {
    color: 'red',
    fontSize: 16,
  },
  container : {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
  imageGallery:{
    display: 'flex',
    flexDirection: 'row',
    width: '100%',
    border: '1px solid black',
    minHeight: '300px',
    padding: '10px',
    marginTop: '10px',
  },
  loader: {
    margin:'125px auto',
    border: '4px solid #f3f3f3',
    borderTop: '4px solid #3498db',
    borderRadius: '50%',
    width: '50px',
    height: '50px',
    animationName: '$spin',
    animationDuration: '2s',
    animationTimingFunction: 'linear',
    animationIterationCount: 'infinite',
  },
  singleImageContainer:{
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    alignItems: 'center',
  }
})


export default useStyles;