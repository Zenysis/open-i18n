// These configurations are used only by jest, our JS unit testing framework.
module.exports = {
  plugins: [],
  presets: [
    '@babel/flow',
    [
      '@babel/preset-env',
      {
        targets: {
          node: 'current',
        },
      },
    ],
    [
      '@babel/react',
      {
        development: true,
      },
    ],
  ],
};
