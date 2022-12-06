odoo.define('thue.chon_ky_tinh_thue_khau_tru_thue_gtgt_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var ChonKyTinhThueKhauTruThueGTGTFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
            var def = defer;
            this.changeSelectionSource('LOAI_TO_KHAI', ['TO_KHAI_THANG','TO_KHAI_QUY']);
            def.resolve();
        },
        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            
            switch (event.data.attrs.id)
            {
                case "btn_dong_y":
                    var context = {
                        'LOAI_CHUNG_TU_DANH_GIA_LAI': 'KHAU_TRU_THUE_GTGT',
                        'LOAI_TO_KHAI': this.getFieldValue('LOAI_TO_KHAI'),
                        'THANG': this.getFieldValue('THANG'),
                        'QUY': this.getFieldValue('QUY'),
                        'NAM': this.getFieldValue('NAM'),
                        };
                    
                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        params: context,
                        readonly: false,
                        res_model: 'account.ex.chung.tu.nghiep.vu.khac',
                        ref_views: [['tong_hop.view_account_ex_chung_tu_nghiep_vu_khac_form', 'form']],
                        title: ("Khấu trừ thuế"),
                        disable_multiple_selection: true,
                        shouldSaveLocally: false,
                    })).open();
                break;
            default: 
                this._super.apply(this, arguments);
            }
        },
    });
    
    var ChonKyTinhThueKhauTruThueGTGTFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: ChonKyTinhThueKhauTruThueGTGTFormController,
        }),
    });
    
    view_registry.add('chon_ky_tinh_thue_khau_tru_thue_gtgt_form_view', ChonKyTinhThueKhauTruThueGTGTFormView);
    
    return ChonKyTinhThueKhauTruThueGTGTFormView;
});

