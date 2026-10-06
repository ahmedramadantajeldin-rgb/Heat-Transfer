/*
 * Chapter registry — the only file you need to edit to add or update a chapter.
 *
 * ADDING A CHAPTER (example: Chapter 3)
 *   1. Put the files in "Chapter 3/" (page: chapter3.html, images: "Chapter 3/images/").
 *   2. In the entry below, change status to 'available' and fill in:
 *        title, description, topics (optional), sections (optional)
 *        href: 'Chapter 3/chapter3.html'
 *   3. Save. The card, its "Open Chapter" button, and the hero shortcut update automatically.
 *
 * To announce a new chapter before it is ready, add an entry with
 *   { number: N, status: 'coming-soon' }
 *
 * Fields
 *   number       Chapter number (cards are sorted by this).
 *   status       'available'   -> card is active and links to href
 *                'coming-soon' -> card is shown as a disabled placeholder (no link)
 *   href         Path to the chapter page, relative to index.html. Required when available.
 *   title        Chapter title (English).
 *   description  One or two sentences about the chapter.
 *   topics       Short list of topic tags shown on the card. Optional.
 *   sections     Number of sections in the chapter, shown on the card. Optional.
 */
window.CHAPTERS = [
  {
    number: 1,
    status: 'available',
    href: 'Chapter 1/chapter1.html',
    title: 'Introduction and Basic Concepts',
    description:
      'Thermodynamics, heat transfer mechanisms, energy balance, conduction, convection, and radiation.',
    topics: [
      "Fourier's law",
      "Newton's law of cooling",
      'Stefan\u2013Boltzmann law',
      'Thermal conductivity',
      'Thermal diffusivity',
      'Prevention through Design (PtD)'
    ],
    sections: 17
  },
  {
    number: 3,
    status: 'available',
    href: 'Chapter 3/chapter3.html',
    title: 'Steady Heat Conduction',
    description:
      'Thermal resistance networks, cylinders and spheres, critical radius of insulation, fins, and building heat transfer.',
    topics: [
      'Thermal resistance',
      'Contact resistance',
      'Composite walls',
      'Critical radius',
      'Fin efficiency',
      'Heat sinks'
    ],
    sections: 14
  }
];
