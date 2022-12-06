odoo.define('bao_cao.bao_cao_chi_tiet_cong_no_phai_thu_khach_hang_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var BaoCaoChiTietCongNoPhaiThuKhachHangController = FormController.extend({
        onFieldChanged: function (field) {
            var domain = [];
            var val = false;
            switch (field) {
                case 'NHOM_KHACH_HANG_ID':
                    val = this.getFieldValue('MA_PC_NHOM_KH');
                    if (val) {
                        domain = [
                            ['LIST_MPC_NHOM_KH_NCC', '=like', '%' + val + '%']
                        ];
                    }
                    this.getFieldWidget('KHACH_HANG_MANY_IDS').changeDomain(domain);
                    break;
                default:
                    break;
            }
            console.log(val);
        },

    });

    var BaoCaoChiTietCongNoPhaiThuKhachHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: BaoCaoChiTietCongNoPhaiThuKhachHangController,
        }),
    });

    view_registry.add('bao_cao_chi_tiet_cong_no_phai_thu_khach_hang_view', BaoCaoChiTietCongNoPhaiThuKhachHangView);
    return BaoCaoChiTietCongNoPhaiThuKhachHangView;
});