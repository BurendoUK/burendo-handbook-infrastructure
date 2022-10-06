import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: '',
    Svg: require('@site/static/img/Burendo_Portrait_RGB.svg').default,
    // description: (
    //   <>
    //     Docusaurus lets you focus on your docs, and we&apos;ll do the chores. Go
    //     ahead and move your docs into the <code>docs</code> directory.
    //   </>
    // ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--12')}>
      <div
        style={{
          justifyContent: 'center',
          alignItems: 'center',
        }}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
