odoo.define('tien_luong.tien_luong_lich_su_tra_luong_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
   
    var TienLuongLichSuTraLuongController = FormController.extend({
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def = defer;
			// var pr = self.params.tham_so;
			// if(pr.kho_id){
			//     self.changeFieldValue('KHO_ID', pr.kho_id);
			// }
            this.rpc_action({
                model: 'tien.luong.lich.su.tra.luong.form',
                method: 'lay_du_lieu_lich_su_tra_luong',
                // args: {
                //     'kho_id' : pr.kho_id,
                // },
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }
					if (def) {
                        def.resolve();
                    }
                }
            });
        },
    });
    
    var TienLuongLichSuTraLuongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongLichSuTraLuongController,
        }),
    });
    
    view_registry.add('tien_luong_lich_su_tra_luong_view', TienLuongLichSuTraLuongView);
    
    return TienLuongLichSuTraLuongView;
});
