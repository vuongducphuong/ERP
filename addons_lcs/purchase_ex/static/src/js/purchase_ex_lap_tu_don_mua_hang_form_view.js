odoo.define('purchase_ex.lap_tu_don_mua_hang_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');


    var LapTuDonMuaHangFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            if (defer) {
                defer.resolve();
            }
        },

        onFieldChanged: function(field){
            var self = this;
            if(field =="SO_DON_HANG_ID")
            {
                var so_don_hang = this.getFieldValue(field);
                var so_don_hang_id = 0;
                if (so_don_hang){
                    so_don_hang_id = so_don_hang.id;
                }
                var loai_chung_tu_mua_hang = self.params.tham_so[0];
                var loai_tien_ct_mua_hang = self.params.tham_so[1];
                this.rpc_action({
                    model: 'purchase.ex.lap.tu.don.mua.hang.form',
                    method: 'thuc_hien_lay_du_lieu_cac_chung_tu',
                    args: {'so_don_hang_id':so_don_hang_id ,'loai_chung_tu_mua_hang' : loai_chung_tu_mua_hang,'loai_tien_ct_mua_hang' : loai_tien_ct_mua_hang},
                    callback: function(result) {
                        if (result) {
                            self.updateUI({'PURCHASE_EX_LAP_TU_DON_MUA_HANG_CHI_TIET_IDS': result});
                            }   
                        }
                    });
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
                    var nha_cung_cap_id;
                    var tu_ngay;
                    var den_ngay;
                    if(null==this.getFieldValue('NHA_CUNG_CAP_ID')){
                        error = '<Nhà cung cấp> không được bỏ trống';

                    }
                    else{
                        nha_cung_cap_id = this.getFieldValue('NHA_CUNG_CAP_ID').id;
                        tu_ngay = this.getFieldValue('TU_NGAY');
                        den_ngay = this.getFieldValue('DEN_NGAY');
                        var loai_chung_tu_mua_hang = self.params.tham_so[0];
                        var loai_tien_ct_mua_hang = self.params.tham_so[1];
                        this.rpc_action({
                            model: 'purchase.ex.lap.tu.don.mua.hang.form',
                            method: 'thuc_hien_lay_du_lieu_cac_chung_tu',
                            args: {'nha_cung_cap_id': nha_cung_cap_id, 'tu_ngay': tu_ngay, 'den_ngay':den_ngay ,'loai_chung_tu_mua_hang' : loai_chung_tu_mua_hang,'loai_tien_ct_mua_hang' : loai_tien_ct_mua_hang},
                            callback: function(result) {
                                if(result){
                                    self.updateUI({'PURCHASE_EX_LAP_TU_DON_MUA_HANG_CHI_TIET_IDS': result});
                                }
                            }
                         });
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

    var LapTuDonMuaHangFormRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var LapTuDonMuaHangFormModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var LapTuDonMuaHangFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: LapTuDonMuaHangFormModel,
            Renderer: LapTuDonMuaHangFormRenderer,
            Controller: LapTuDonMuaHangFormController,
        }),
    });
    
    view_registry.add('lap_tu_don_mua_hang_form_view', LapTuDonMuaHangFormView);
    
    return LapTuDonMuaHangFormView;
});
