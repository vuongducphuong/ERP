odoo.define('danh_muc.danh_muc_danh_sach_chung_tu_phat_sinh_ma_quy_cach', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var DanhMucDSCTPhatSinhMQCController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def = defer;
            this.rpc_action({
                model: 'danh.muc.dsct.phat.sinh.ma.quy.cach.form',
                method: 'lay_danh_sach_ma_quy_cach',
                args: {'ma_vat_tu_hang_hoa': e.ma_san_pham},
                callback: function(result) {
                    if (result) {
						self.updateUI({'DANH_MUC_DSCT_PHAT_SINH_MA_QUY_CACH_CHI_TIET_IDS': result});
                    }
					if (def) {
                        def.resolve();
                    }					
                }
            });
        },
        
    });

    var DanhMucDSCTPhatSinhMQCRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var DanhMucDSCTPhatSinhMQCModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var DanhMucDSCTPhatSinhMQCView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: DanhMucDSCTPhatSinhMQCModel,
            Renderer: DanhMucDSCTPhatSinhMQCRenderer,
            Controller: DanhMucDSCTPhatSinhMQCController,
        }),
    });
    
    view_registry.add('danh_muc_danh_sach_chung_tu_phat_sinh_ma_quy_cach', DanhMucDSCTPhatSinhMQCView);
    
    return DanhMucDSCTPhatSinhMQCView;
});
