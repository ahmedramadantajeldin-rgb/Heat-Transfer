/*
 * Course data. To add or publish a chapter, edit only this file:
 *   1. Put the chapter in its own folder, e.g. "Chapter 3/chapter3.html" and "Chapter 3/images/".
 *   2. Change its status below from "coming-soon" to "available" and set href.
 * Fields: number, title (optional), titleAr (optional), summary (optional),
 *         topics (optional list), sections (optional count), status, href (required when available).
 */
window.COURSE = {
  title: "Heat Transfer",
  subtitle: "Heat transfer mechanisms, energy balance, and the laws of conduction, convection, and radiation."
};

window.CHAPTERS = [
  {
    number: 1,
    title: "Introduction and Basic Concepts",
    titleAr: "مقدمة والمفاهيم الأساسية",
    summary: "Thermodynamics and heat transfer, energy balance and the first law, then conduction, convection, and radiation.",
    topics: ["Conduction", "Convection", "Radiation", "Energy balance", "Thermal conductivity"],
    sections: 17,
    status: "available",
    href: "Chapter 1/chapter1.html"
  },
  {
    number: 3,
    summary: "This chapter is under development and will be added later.",
    status: "coming-soon"
  }
];
