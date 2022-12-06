odoo.define('bao_cao.bao_cao_tinh_hinh_thuc_hien_don_dat_hang_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoTinhHinhThucHienDonDatHangController = FormController.extend({
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
                case 'NHOM_KH_ID':
                    val = this.getFieldValue('MA_PC_NHOM_KH');
                    if (val) {
                        domain = [['LIST_MPC_NHOM_KH_NCC','=like', '%'+val+'%']];
                    }
                    this.getFieldWidget('KHACH_HANG_MANY_IDS').changeDomain(domain);
                    break;
            
                default:
                    break;
            }
            console.log(val);
        },
       
    });   
    
    var BaoCaoTinhHinhThucHienDonDatHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoTinhHinhThucHienDonDatHangController,
        }),
    });
    
    view_registry.add('bao_cao_tinh_hinh_thuc_hien_don_dat_hang_view', BaoCaoTinhHinhThucHienDonDatHangView);
    return BaoCaoTinhHinhThucHienDonDatHangView;
});
