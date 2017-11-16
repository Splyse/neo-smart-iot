/**
 * Action.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {
    contractId: {
      type: 'integer',
      required: true
    },
    name: { // TODO: make unique so owners can't duplicate contracts to mislead users
      type: 'string',
      required: true
    },
    description: {
      type: 'string',
      required: true
    },
    type: { // can be one of text, toggle, etc
      type: 'string',
      required: true
    },
    price: { // can be one of text, toggle, etc
      type: 'string',
      required: true
    },
    scriptHash: { // can be one of text, toggle, etc
      type: 'string',
      required: true
    },
  }
};
