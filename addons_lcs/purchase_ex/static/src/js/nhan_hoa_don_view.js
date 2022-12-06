odoo.define('purchase_ex.nhan_hoa_don_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var NhanHoaDonController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            event.stopPropagation();
            var self = this;
            var def = $.Deferred();
            var error = [];
            switch (event.data.attrs.name)
            {
                
                case "btn_lay_du_lieu":
                    var doi_tuong_id;
                    var tu_ngay;
                    var den_ngay;
                    if(this.getFieldValue('DOI_TUONG_ID')){
                        doi_tuong_id = this.getFieldValue('DOI_TUONG_ID').id;
                    }else{
                        error = 'Bạn phải chọn đối tượng';
                    };
                    if(this.getFieldValue('TU')){
                        tu_ngay = this.getFieldValue('TU');
                    }else{
                        error = 'Bạn phải chọn từ ngày';
                    };
                    if(this.getFieldValue('DEN')){
                        den_ngay = this.getFieldValue('DEN');
                    }else{
                        error = 'Bạn phải chọn từ ngày';
                    };
                    if (error.length) {
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                        return def;
                    } else {
                        def.resolve(true);
                    }
                    this.rpc_action({
                        model: 'purchase.ex.nhan.hoa.don',
                        method: 'lay_du_lieu_hoa_don',
                        args: {
                            'doi_tuong_id' : doi_tuong_id,
                            'tu_ngay' : tu_ngay,
                            'den_ngay' : den_ngay,
                        },
                        callback: function(result) {
                            if (result) {
                                self.updateUI({'PURCHASE_EX_NHAN_HOA_DON_CHI_TIET_IDS':result});
                            }
                        }
                    });
                    break;
                
                default: 
                   this._super.apply(this, arguments);
            }
                 
            
        }
    });
    
    var NhanHoaDonFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: NhanHoaDonController,
        }),
    });
    
    view_registry.add('nhan_hoa_don_view', NhanHoaDonFormView);
    
    return NhanHoaDonFormView;
});
