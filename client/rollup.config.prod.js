import typescript from '@rollup/plugin-typescript';
import commonjs from '@rollup/plugin-commonjs';
import babel from '@rollup/plugin-babel';
import resolve from '@rollup/plugin-node-resolve';
import livereload from 'rollup-plugin-livereload';
import serve from 'rollup-plugin-serve';
import replace from '@rollup/plugin-replace';

export default {
  input: 'src/index.tsx',
  output: {
    file: 'dist/bundle.js',
    format: 'iife',
    sourcemap: true
  },
  plugins: [
    typescript({
      tsconfig: 'tsconfig.json'
    }),
    resolve({
      browser: true
    }),
    commonjs(),
    babel({ babelHelpers: 'bundled' }),
    replace({
      preventAssignment: true,
      'process.env.NODE_ENV': JSON.stringify( 'production' )
    })
  ]
};
