/* Determines what ribbons should be hidden while mousing over a group */
export var isHiddenRibbon = function isHiddenRibbon(mouseOverGroup, sourceIndex, targetIndex) {

    return mouseOverGroup !== null ? mouseOverGroup !== sourceIndex && mouseOverGroup !== targetIndex : false;
};