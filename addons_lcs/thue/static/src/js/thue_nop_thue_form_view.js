odoo.define('thue.nop_thue_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var NopThueFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onButtonClicked: function(event) {
            event.stopPropagation();
            var self = this;
            
            switch (event.data.attrs.id)
            {
                case "btn_nop_thue":
                    var context = {};
                    var ref_views = [[]];
                    var title ='';
                    var phuong_thuc_thanh_toan = this.getFieldValue('PHUONG_THUC_THANH_TOAN');
                    if (phuong_thuc_thanh_toan == 'TIEN_GUI' ){
                        context = {
                            'LOAI_CHUNG_TU_TEMPLE': 1512,
                            'TYPE_NH_Q': 'NGAN_HANG',
                            'LOAI_PHIEU': 'PHIEU_CHI',
                            };
                        ref_views = [['account_ex.action_account_ex_ngan_hang_phieu_chi_tien', 'form']];
                        title = 'Chi tiền gửi nộp thuế';
                    }
                    else if (phuong_thuc_thanh_toan == 'TIEN_MAT' ){
                        context = {
                            'LOAI_CHUNG_TU_TEMPLE': 1022,
                            'TYPE_NH_Q': 'QUY',
                            'LOAI_PHIEU': 'PHIEU_CHI',
                            };

                        ref_views = [['account_ex.action_account_ex_quy_phieu_chi_tien', 'form']];
                        title = 'Phiếu chi nộp thuế';
                    }
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        params: context,
                        readonly: false,
                        res_model: 'account.ex.phieu.thu.chi',
                        ref_views: ref_views,
                        title: title,
                        disable_multiple_selection: true,
                        shouldSaveLocally: false,
                    })).open();
                    break;
                default: 
                this._super.apply(this, arguments);
            }
        },
    });
    
    var NopThueFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: NopThueFormController,
        }),
    });
    
    view_registry.add('nop_thue_form_view', NopThueFormView);
    
    return NopThueFormView;
});

