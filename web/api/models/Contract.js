/**
 * Contract.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {
    name: { // TODO: make unique so owners can't duplicate contracts to mislead users
      type: 'string',
      required: true
    },
    description: {
      type: 'string',
      required: true
    },
    ownerEmail: {
      type: 'email',
      required: true
    }
  }
};
