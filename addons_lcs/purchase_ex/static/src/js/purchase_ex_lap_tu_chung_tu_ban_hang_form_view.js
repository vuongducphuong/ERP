odoo.define('purchase_ex.lap_tu_chung_tu_ban_hang_fom_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var LapTuChungTuBanHangFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            if (defer) {
                defer.resolve();
            }
        },

        _onButtonClicked: function(event) {
            var self = this;
            event.stopPropagation();
            var def = $.Deferred();
            var error = [];
            switch (event.data.attrs.id)
            {
                case "btn_lay_du_lieu":
                    var tu_ngay;
                    var den_ngay;
                    var chi_nhanh_id;
                    var khach_hang_id;

                    if (null==this.getFieldValue('CHI_NHANH_ID') || null==this.getFieldValue('KHACH_HANG_ID')){
                        khach_hang_id = null;
                        chi_nhanh_id= null;
                    }
                    else{

                        khach_hang_id = this.getFieldValue('KHACH_HANG_ID').id;
                        chi_nhanh_id= this.getFieldValue('CHI_NHANH_ID').id;
                    }

                    if(null==this.getFieldValue('TU_NGAY')){
                        error = '<Từ ngày> không được bỏ trống.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                        
                    }
                    else{
                        if(null==this.getFieldValue('DEN_NGAY')){
                            error = '<Đến ngày> không được bỏ trống.';
                            self.notifyInvalidFields(error);
                            def.resolve(false);
                            
                        }
                        else{
                            tu_ngay = this.getFieldValue('TU_NGAY');
                            den_ngay = this.getFieldValue('DEN_NGAY');
                            this.rpc_action({
                                model: 'purchase.ex.lap.tu.chung.tu.ban.hang.form',
                                method: 'thuc_hien_lay_du_lieu_cac_chung_tu',
                                args: {'chi_nhanh_id':chi_nhanh_id,'khach_hang_id':khach_hang_id,'tu_ngay': tu_ngay, 'den_ngay':den_ngay },
                                callback: function(result) {
                                    if(result){
                                        
                                        self.updateUI({'PURCHASE_EX_LAP_TU_CHUNG_TU_BAN_HANG_FORM_CHI_TIET_IDS': result});
                                    }
                                }
                             });
                        }
                    }
                    def.resolve(true);
                    return def;
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    var LapTuChungTuBanHangFormRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var LapTuChungTuBanHangFormModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var LapTuChungTuBanHangFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: LapTuChungTuBanHangFormModel,
            Renderer: LapTuChungTuBanHangFormRenderer,
            Controller: LapTuChungTuBanHangFormController,
        }),
    });
    
    view_registry.add('lap_tu_chung_tu_ban_hang_fom_view', LapTuChungTuBanHangFormView);
    
    return LapTuChungTuBanHangFormView;
});
