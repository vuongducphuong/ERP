odoo.define('stock_ex.chung_tu_luu_ma_quy_cach_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var ChungTuLuuMaQuyCachController = FormController.extend({
        onViewLoaded: function(e, defer) {
            var self = this;
			var def = defer;
            this.rpc_action({
                model: 'stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form',
                method: 'lay_chung_tu_luu_ma_quy_cach',
                // args: {},
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }
					if (def) {
                        def.resolve();
                    }					
                }
            });
        }
    });
    
    var ChungTuLuuMaQuyCachView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: ChungTuLuuMaQuyCachController,
        }),
    });
    
    view_registry.add('chung_tu_luu_ma_quy_cach_form_view', ChungTuLuuMaQuyCachView);
    
    return ChungTuLuuMaQuyCachView;
});