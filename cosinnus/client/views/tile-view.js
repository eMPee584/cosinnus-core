'use strict';

var BaseView = require('views/base/view');
var Result = require('models/result');
var util = require('lib/util');

var tileTemplate = require('tiles/tile');
var detailTemplate = require('tiles/tile-detail');

module.exports = BaseView.extend({
	
	// reference back to the main App
	App: null,
	
	model: Result,

	template: tileTemplate,
	
	// The DOM events specific to an item.
    events: {
        'click .tile-detail-link': 'onSelectClicked',
        'click .tile-close-button': 'onDeselectClicked',

        'mouseenter': 'onMouseEnter',
        'mouseleave': 'onMouseLeave',
    },
	
    initialize: function (options, app) {
        var self = this;
    	BaseView.prototype.initialize.call(self, options);
    	self.App = app;
    	
    	self.model.on({
    		'change:selected': self.thisContext(self.onSelectChanged),
    		'change:hovered': self.thisContext(self.onHoverChanged),
    	});
    },
    
    /**
     * Called when the .selected property of the Result model was changed.
     * We actually do the display and re-render here, because
     * the selected change may be triggered in other views.
     */
    onSelectChanged: function () {
    	if (this.model.get('selected') == true) {
    		// clear hover on this to not confuse styles
    		this.App.controlView.setHoveredResult(null);
    		this.template = detailTemplate;
    		$('.tile-list').addClass('tile-detail-open');
    	} else {
    		this.template = tileTemplate;
    		$('.tile-list').removeClass('tile-detail-open');
    	}
    	this.render();
    },
    
    /**
     * Called when the .hovered property of the Result model was changed.
     * We actually do the display and re-render here, because
     * the selected change may be triggered in other views.
     */
    onHoverChanged: function () {
		this.$el.toggleClass('hovered', this.model.get('hovered'));
    },
    
    
    onMouseEnter: function() {
    	if (!this.model.get('selected')) {
    		util.log('tile-view.js: got a hover event! id: ' + this.model.id);
    		this.App.controlView.setHoveredResult(this.model);
    	}
    },
    onMouseLeave: function() {
    	if (!this.model.get('selected')) {
	    	util.log('tile-view.js: got an unhover event! id: ' + this.model.id);
	    	this.App.controlView.setHoveredResult(null);
    	}
    },
    
    
    /**
     * Called when a tile detail link is clicked, to expand the tile view
     * to the full size detail view.
     * We only change the Result model's .selected property and
     * don't do any rendering here.
     */
    onSelectClicked: function () {
    	util.log('tile-view.js: got a select click event! id: ' + this.model.id);
    	this.App.controlView.setSelectedResult(this.model);
    },
    
    /**
     * Called when a tile detail close button is clicked.
     * We only change the Result model's .selected property and
     * don't do any rendering here.
     */
    onDeselectClicked: function () {
    	util.log('tile-view.js: got a deselect click event! id: ' + this.model.id);
    	this.App.controlView.setSelectedResult(null);
    },
    
});