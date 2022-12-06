odoo.define('sale_ex.bo_doi_tru_chung_tu_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');
    
    var BoDoiTruChungTuFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            var self = this;
            event.stopPropagation();
            var def = $.Deferred();
            var error = [];
            switch (event.data.attrs.id)
            {
                
                case "btn_bo_doi_tru":
                    var tham_so = {};
                    var default_chi_tiet = [];
                    var current_data = event.data.record.data;
                    // tham_so = {
                    //     'currency_id' : current_data.currency_id.data.id,
                    // }
                    // self.changeFieldValue('BO_DOI_TRU_JSON', tham_so);
                    this.rpc_action({
                        model: 'sale.ex.bo.doi.tru',
                        method: 'bo_doi_tru',
                        // args: {
                        //     'tai_khoan_id' : pr.tai_khoan_id,
                        // },
                        callback: function(result) {
                            if (result) {
                                self.updateUI({'SALE_EX_BO_DOI_TRU_CHI_TIET_IDS': result});
                            }
                        }
                    });
                    break;

                
                case "btn_lay_du_lieu":
                    var loai_bo_doi_tru = this.getFieldValue('LOAI_BO_DOI_TRU')
                    if (loai_bo_doi_tru == 'BAN_HANG'){
                        if(null==this.getFieldValue('TAI_KHOAN_THU_ID')){
                            error.push({field:'TAI_KHOAN_THU_ID', message:'<Tài khoản phải thu> không được bỏ trống.'});
                        }
                        else if(null==this.getFieldValue('KHACH_HANG_ID')){
                            error.push({field:'KHACH_HANG_ID', message:'<Khách hàng> không được bỏ trống.'});
                        }
                        else if(null==this.getFieldValue('currency_id')){
                            error.push({field:'currency_id', message:'<Loại tiền> không được bỏ trống.'});
                        }
                        else{
                            this.rpc_action({
                                model: 'sale.ex.bo.doi.tru',
                                method: 'lay_du_lieu_doi_tru',
                                callback: function(result) {
                                    if(result){
                                        self.updateUI({'SALE_EX_BO_DOI_TRU_CHI_TIET_IDS': result});
                                    }
                                }
                                });

                        }
                    }
                    else if (loai_bo_doi_tru == 'MUA_HANG'){
                        if(null==this.getFieldValue('TAI_KHOAN_TRA_ID')){
                            error.push({field:'TAI_KHOAN_TRA_ID', message:'<Tài khoản phải trả> không được bỏ trống.'});
                        }
                        else if(null==this.getFieldValue('NHA_CUNG_CAP_ID')){
                            error.push({field:'NHA_CUNG_CAP_ID', message:'<Nhà cung cấp> không được bỏ trống.'});
                        }
                        else if(null==this.getFieldValue('currency_id')){
                            error.push({field:'currency_id', message:'<Loại tiền> không được bỏ trống.'});
                        }
                        else{
                            this.rpc_action({
                                model: 'sale.ex.bo.doi.tru',
                                method: 'lay_du_lieu_doi_tru',
                                callback: function(result) {
                                    if(result){
                                        self.updateUI({'SALE_EX_BO_DOI_TRU_CHI_TIET_IDS': result});
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
    
    var BoDoiTruChungTuFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BoDoiTruChungTuFormController,
        }),
    });
    
    view_registry.add('bo_doi_tru_chung_tu_form_view', BoDoiTruChungTuFormView);
    
    return BoDoiTruChungTuFormView;
});
