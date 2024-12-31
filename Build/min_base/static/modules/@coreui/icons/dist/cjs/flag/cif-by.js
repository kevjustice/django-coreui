'use strict';

var cifBy = ["301 151", "<g fill='none'><path fill='#C8313E' d='M.5.5h300v150H.5z'/><path fill='#4AA657' d='M.5 100.5h300v50H.5z'/><path fill='#FFF' d='M.5.5h33.333v150H.5z'/><path fill='#C8313E' d='M6.297.5h4.348v2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.45v2.459h-1.45v2.459h-1.449v2.459h-1.449v2.459h-1.449v2.459H9.196v2.459H7.747v-2.459h-1.45v-2.459H4.848v-2.459H3.399v-2.459H1.95v-2.459H.5v-2.459h1.449V7.877h1.449V5.418h1.449V2.959h1.449V.5h.001zm1.45 4.918h1.449v2.459h1.449v2.459h1.449v2.459h-1.449v2.459H9.196v2.459H7.747v-2.459h-1.45v-2.459H4.848v-2.459h1.449V7.877h1.45V5.418zm0 4.918h1.449v2.459H7.747v-2.459zM.5 2.959h1.449v2.459H.5V2.959zm0 14.754h1.449v2.459H.5v-2.459zM16.442.5h.869v4.918h-.869V.5zm0 17.213h.869v4.918h-.869v-4.918zM3.399 22.631h1.449v2.459h1.449v2.459h1.45v2.459h-1.45v2.459H4.848v2.459H3.399v-2.459H1.95v-2.459H.5v-2.459h1.449V25.09h1.449v-2.459h.001zm0 4.918h1.449v2.459H3.399v-2.459zm8.695-4.918h1.449v2.459h1.449v2.459h1.45v2.459h-1.45v2.459h-1.449v2.459h-1.449v-2.459h-1.449v-2.459H9.196v-2.459h1.449V25.09h1.449v-2.459zm0 4.918h1.449v2.459h-1.449v-2.459zM.5 37.385h1.449v2.459H.5v-2.459zm15.942-2.459h.869v4.918h-.869v-4.918zM.5 44.762h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.45v-2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.45v2.459h.869v9.836h-.869v2.459h-1.45v2.459h-1.449v2.459h-1.449v2.459h-1.449v2.459H9.195v6.394H6.296V74.27H4.847v-2.459H3.398v-2.459H1.949v-2.459H.5v-7.377h1.449v2.459h1.449v2.459h1.449v2.459h1.449v-2.459h1.45v-2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h-1.449V49.68h-1.449v-2.459H6.296v2.459h2.899v2.459H7.746v2.459h-1.45v2.459H4.847v-2.459H3.398v-2.459H1.949V49.68H.5v-4.918zm0 9.836h1.449v2.459H.5v-2.459zm15.942 7.377h.869v2.459h-.869v-2.459zm-2.898 4.918h1.449v2.459h1.45v2.459h.869v3.935h-.869V74.27h-1.45v-2.459h-1.449v-4.918zm-2.899 7.377h1.449v1.476h-1.449V74.27z'/><path fill='#C8313E' d='M28.036.5h-4.348v2.459h-1.45v2.459h-1.449v2.459H19.34v2.459h-1.449v2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.45v2.459h1.449v2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.45v-2.459h1.449v-2.459h-1.449V7.877h-1.45V5.418h-1.449V2.959h-1.449V.5h.001zm-1.449 4.918h-1.449v2.459h-1.449v2.459h-1.45v2.459h1.45v2.459h1.449v2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h-1.449V7.877h-1.449V5.418zm0 4.918h-1.449v2.459h1.449v-2.459zm7.247-7.377h-1.449v2.459h1.449V2.959zm0 14.754h-1.449v2.459h1.449v-2.459zM17.892.5h-.869v4.918h.869V.5zm0 17.213h-.869v4.918h.869v-4.918zm13.043 4.918h-1.449v2.459h-1.449v2.459h-1.449v2.459h1.449v2.459h1.449v2.459h1.449v-2.459h1.45v-2.459h1.449v-2.459h-1.449V25.09h-1.45v-2.459zm0 4.918h-1.449v2.459h1.449v-2.459zm-8.696-4.918H20.79v2.459h-1.449v2.459h-1.449v2.459h1.449v2.459h1.449v2.459h1.449v-2.459h1.45v-2.459h1.449v-2.459h-1.449V25.09h-1.45v-2.459zm0 4.918H20.79v2.459h1.449v-2.459zm11.595 9.836h-1.449v2.459h1.449v-2.459zm-15.942-2.459h-.869v4.918h.869v-4.918zM33.834 44.762h-1.449v-2.459h-1.45v-2.459h-1.449v-2.459h-1.449v-2.459h-1.449v-2.459h-1.449v2.459H23.69v2.459h-1.45v2.459h-1.449v2.459h-1.449v2.459h-1.449v2.459h-.869v9.836h.869v2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.45v2.459h1.449v6.394h2.898V74.27h1.449v-2.459h1.449v-2.459h1.45v-2.459h1.449v-7.377h-1.449v2.459h-1.45v2.459h-1.449v2.459h-1.449v-2.459h-1.449v-2.459h-1.449v-2.459H23.69v-2.459h-1.45v-2.459h-1.449v-2.459h1.449V49.68h1.45v-2.459h4.348v2.459H25.14v2.459h1.449v2.459h1.449v2.459h1.449v-2.459h1.449v-2.459h1.45V49.68h1.449v-4.918h-.001zm0 9.836h-1.449v2.459h1.449v-2.459zm-15.942 7.377h-.869v2.459h.869v-2.459zm2.898 4.918h-1.449v2.459h-1.449v2.459h-.869v3.935h.869V74.27h1.449v-2.459h1.449v-4.918zm2.899 7.377h-1.45v1.476h1.45V74.27z'/><path fill='#FCFCFC' d='M9.255 17.63H7.806v-2.459H6.357v-2.459H4.908v-2.459h1.449V7.794h1.449V5.335h1.449v2.459h1.45v2.459h1.449v2.459h-1.449v2.459h-1.45zM26.652 17.63h-1.449v-2.459h-1.449v-2.459h-1.45v-2.459h1.45V7.794h1.449V5.335h1.449v2.459h1.45v2.459h1.449v2.459h-1.449v2.459h-1.45z'/><path fill='#C8313E' d='M7.806 10.253h1.449v2.459H7.806zM25.138 10.336h1.449v2.459h-1.449z'/><path fill='#FFF' d='M29.551 27.676H31v2.459h-1.449zM20.747 27.503h1.449v2.459h-1.449z'/><path fill='#FFFDFD' d='M12.154 27.503h1.449v2.459h-1.449z'/><path fill='#FFF' d='M3.458 27.503h1.449v2.459H3.458z'/><path fill='#C8313E' d='M6.297 150.5h4.348v-2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.45v-2.459h-1.45v-2.459h-1.449v-2.459h-1.449v-2.459h-1.449v-2.459H9.196v-2.459H7.747v2.459h-1.45v2.459H4.848v2.459H3.399v2.459H1.95v2.459H.5v2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.449v2.459h.001zm1.45-4.918h1.449v-2.459h1.449v-2.459h1.449v-2.459h-1.449v-2.459H9.196v-2.459H7.747v2.459h-1.45v2.459H4.848v2.459h1.449v2.459h1.45v2.459zm0-4.918h1.449v-2.459H7.747v2.459zM.5 148.041h1.449v-2.459H.5v2.459zm0-14.754h1.449v-2.459H.5v2.459zM16.442 150.5h.869v-4.918h-.869v4.918zm0-17.213h.869v-4.918h-.869v4.918zm-13.043-4.918h1.449v-2.459h1.449v-2.459h1.45v-2.459h-1.45v-2.459H4.848v-2.459H3.399v2.459H1.95v2.459H.5v2.459h1.449v2.459h1.449v2.459h.001zm0-4.918h1.449v-2.459H3.399v2.459zm8.695 4.918h1.449v-2.459h1.449v-2.459h1.45v-2.459h-1.45v-2.459h-1.449v-2.459h-1.449v2.459h-1.449v2.459H9.196v2.459h1.449v2.459h1.449v2.459zm0-4.918h1.449v-2.459h-1.449v2.459zM.5 113.615h1.449v-2.459H.5v2.459zm15.942 2.459h.869v-4.918h-.869v4.918zM.5 106.238h1.449v2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.45v2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.45v-2.459h.869v-9.836h-.869v-2.459h-1.45v-2.459h-1.449v-2.459h-1.449v-2.459h-1.449v-2.459H9.195v-6.394H6.296v1.475H4.847v2.459H3.398v2.459H1.949v2.459H.5v7.377h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.449v2.459h1.45v2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.449v2.459h-1.449v2.459h-1.449v2.459H6.296v-2.459h2.899V98.86H7.746v-2.459h-1.45v-2.459H4.847v2.459H3.398v2.459H1.949v2.459H.5v4.919zm0-9.837h1.449v-2.459H.5v2.459zm15.942-7.377h.869v-2.459h-.869v2.459zm-2.898-4.917h1.449v-2.459h1.45v-2.459h.869v-3.934h-.869v1.475h-1.45v2.459h-1.449v4.918zm-2.899-7.378h1.449v-1.475h-1.449v1.475z'/><path fill='#C8313E' d='M28.036 150.5h-4.348v-2.459h-1.45v-2.459h-1.449v-2.459H19.34v-2.459h-1.449v-2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.45v-2.459h1.449v-2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.449v2.459h1.45v2.459h1.449v2.459h-1.449v2.459h-1.45v2.459h-1.449v2.459h-1.449v2.459h.001zm-1.449-4.918h-1.449v-2.459h-1.449v-2.459h-1.45v-2.459h1.45v-2.459h1.449v-2.459h1.449v2.459h1.449v2.459h1.449v2.459h-1.449v2.459h-1.449v2.459zm0-4.918h-1.449v-2.459h1.449v2.459zm7.247 7.377h-1.449v-2.459h1.449v2.459zm0-14.754h-1.449v-2.459h1.449v2.459zM17.892 150.5h-.869v-4.918h.869v4.918zm0-17.213h-.869v-4.918h.869v4.918zm13.043-4.918h-1.449v-2.459h-1.449v-2.459h-1.449v-2.459h1.449v-2.459h1.449v-2.459h1.449v2.459h1.45v2.459h1.449v2.459h-1.449v2.459h-1.45v2.459zm0-4.918h-1.449v-2.459h1.449v2.459zm-8.696 4.918H20.79v-2.459h-1.449v-2.459h-1.449v-2.459h1.449v-2.459h1.449v-2.459h1.449v2.459h1.45v2.459h1.449v2.459h-1.449v2.459h-1.45v2.459zm0-4.918H20.79v-2.459h1.449v2.459zm11.595-9.836h-1.449v-2.459h1.449v2.459zm-15.942 2.459h-.869v-4.918h.869v4.918zM33.834 106.238h-1.449v2.459h-1.45v2.459h-1.449v2.459h-1.449v2.459h-1.449v2.459h-1.449v-2.459H23.69v-2.459h-1.45v-2.459h-1.449v-2.459h-1.449v-2.459h-1.449v-2.459h-.869v-9.836h.869v-2.459h1.449v-2.459h1.449v-2.459h1.449v-2.459h1.45v-2.459h1.449v-6.394h2.898v1.475h1.449v2.459h1.449v2.459h1.45v2.459h1.449v7.377h-1.449v-2.459h-1.45v-2.459h-1.449v-2.459h-1.449v2.459h-1.449v2.459h-1.449v2.459H23.69v2.459h-1.45v2.459h-1.449v2.459h1.449v2.459h1.45v2.459h4.348v-2.459H25.14V98.86h1.449v-2.459h1.449v-2.459h1.449v2.459h1.449v2.459h1.45v2.459h1.449v4.919h-.001zm0-9.837h-1.449v-2.459h1.449v2.459zm-15.942-7.377h-.869v-2.459h.869v2.459zm2.898-4.917h-1.449v-2.459h-1.449v-2.459h-.869v-3.934h.869v1.475h1.449v2.459h1.449v4.918zm2.899-7.378h-1.45v-1.475h1.45v1.475z'/><path fill='#FCFCFC' d='M25.078 133.37h1.45v2.459h1.449v2.459h1.449v2.459h-1.449v2.459h-1.449v2.459h-1.45v-2.459h-1.449v-2.459H22.18v-2.459h1.449v-2.459h1.449zM7.682 133.37h1.449v2.459h1.449v2.459h1.449v2.459H10.58v2.459H9.131v2.459H7.682v-2.459h-1.45v-2.459H4.783v-2.459h1.449v-2.459h1.45z'/><path fill='#C8313E' d='M25.078 138.288h1.449v2.459h-1.449zM7.747 138.205h1.449v2.459H7.747z'/><path fill='#FFF' d='M3.334 120.865h1.449v2.459H3.334zM12.138 121.038h1.449v2.459h-1.449z'/><path fill='#FFFDFD' d='M20.73 121.038h1.449v2.459H20.73z'/><path fill='#FFF' d='M29.426 121.038h1.449v2.459h-1.449z'/></g>"];

exports.cifBy = cifBy;
//# sourceMappingURL=cif-by.js.map
