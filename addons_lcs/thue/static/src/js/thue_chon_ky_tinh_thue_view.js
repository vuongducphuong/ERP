odoo.define('thue.chon_ky_tinh_thue_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var ChonKyTinhThueFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
            var def = defer;
            var pr = self.params.tham_so;
            if (pr){
                if (pr.default_KHOAN_MUC_THUE == 'TIEU_THU_DAC_BIET' || pr.default_KHOAN_MUC_THUE == 'THUE_TAI_NGUYEN'){
                    this.changeSelectionSource('LOAI_TO_KHAI', ['TO_KHAI_THANG','TO_KHAI_LAN_PHAT_SINH']);
                }
                else{
                    this.changeSelectionSource('LOAI_TO_KHAI', ['TO_KHAI_THANG','TO_KHAI_QUY']);
                }
                this.rpc_action({
                    model: 'thue.chon.ky.tinh.thue',
                    method: 'lay_danh_sach_phu_luc_ke_khai',
                    args: {
                        'khoan_muc_thue' : pr.default_KHOAN_MUC_THUE,
                    },
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result).then(function(){
                                if (def) {
                                    def.resolve();
                                }
                            });
                        }
                    }
                });
            }
            def.resolve();
        },
       
    });
    
    var ChonKyTinhThueFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: ChonKyTinhThueFormController,
        }),
    });
    
    view_registry.add('chon_ky_tinh_thue_form_view', ChonKyTinhThueFormView);
    
    return ChonKyTinhThueFormView;
});

