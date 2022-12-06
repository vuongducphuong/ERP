odoo.define('bao_cao.bao_cao_so_tong_hop_ban_hang_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoSoTongHopBanHangController = FormController.extend({
        onFieldChanged: function(field) {
            var domain = [];
            var val = false;
            switch (field) {
                case 'NHOM_VTHH_ID':
                    val = this.getFieldValue('MA_PC_NHOM_VTHH');
                    if (val) {
                        domain = [['LIST_MPC_NHOM_VTHH','=like', '%'+val+'%']];
                    }
                    this.getFieldWidget('SAN_PHAM_MANY_IDS').changeDomain(domain);
                    break;
                case 'NHOM_KHACH_HANG_ID':
                    val = this.getFieldValue('MA_PC_NHOM_KH');
                    if (val) {
                        domain = [['LIST_MPC_NHOM_KH_NCC','=like', '%'+val+'%']];
                    }
                    this.getFieldWidget('KHACH_HANG_MANY_IDS').changeDomain(domain);
                    break;
                case 'DON_VI_ID':
                    val = this.getFieldValue(field);
                    if (val.id) {
                        domain = [['DON_VI_ID','=',val.id]];
                    }
                    this.getFieldWidget('NHAN_VIEN_MANY_IDS').changeDomain(domain);
                    break;
            
                default:
                    break;
            }
            console.log(val);
        },
       
    });   
    
    var BaoCaoSoTongHopBanHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoSoTongHopBanHangController,
        }),
    });
    
    view_registry.add('bao_cao_so_tong_hop_ban_hang_view', BaoCaoSoTongHopBanHangView);
    return BaoCaoSoTongHopBanHangView;
});
