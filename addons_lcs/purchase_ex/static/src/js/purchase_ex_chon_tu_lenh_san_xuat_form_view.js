odoo.define('purchase_ex.chon_tu_lenh_san_xuat_fom_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var LapTuLenhSanhXuatFormController = FormController.extend({
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
                case "btn_lay_du_lieu_chon_lenh_san_xuat":
                    var tu_ngay;
                    var den_ngay;
                    if(null==this.getFieldValue('TU_NGAY')){
                        error = '<Từ ngày> không được bỏ trống.';
                    }
                    else{
                        if(null==this.getFieldValue('DEN_NGAY')){
                            error = '<Đến ngày> không được bỏ trống.';
                        }
                        else{
                            tu_ngay = this.getFieldValue('TU_NGAY');
                            den_ngay = this.getFieldValue('DEN_NGAY');
                            this.rpc_action({
                                model: 'purchase.ex.chon.tu.lenh.san.xuat.form',
                                method: 'thuc_hien_lay_du_lieu_cac_chung_tu',
                                args: {'tu_ngay': tu_ngay, 'den_ngay':den_ngay },
                                callback: function(result) {
                                    if(result){
                                        self.updateUI({'PURCHASE_EX_CHON_TU_LENH_SAN_XUAT_FORM_CHI_TIET_IDS': result});
                                    }
                                }
                             });
                        }
                    }
                    if (error.length) {
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    } else {
                        def.resolve(true);
                    }
                    return def;
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    var LapTuLenhSanhXuatFormRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var LapTuLenhSanhXuatFormModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var LapTuLenhSanhXuatFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: LapTuLenhSanhXuatFormModel,
            Renderer: LapTuLenhSanhXuatFormRenderer,
            Controller: LapTuLenhSanhXuatFormController,
        }),
    });
    
    view_registry.add('chon_tu_lenh_san_xuat_fom_view', LapTuLenhSanhXuatFormView);
    
    return LapTuLenhSanhXuatFormView;
});
