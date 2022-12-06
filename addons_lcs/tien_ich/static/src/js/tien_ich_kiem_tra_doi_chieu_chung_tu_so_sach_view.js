odoo.define('tien_ich.kiem_tra_doi_chieu_chung_tu_so_sach_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var KiemTraDoiChieuChungTuSoSachController = FormController.extend({
        onFieldChanged: function(field) {
            if (field=='CHON_BO_TAT_CA') {
                var newValue = this.getFieldValue(field);
                this.updateUI({'TRANG_THAI_GHI_SO_CHUNG_TU':newValue,
                    'TIEN_MAT_TIEN_GUI':newValue,
                    'KHO_MUA_HANG':newValue,
                    'CONG_NO':newValue,
                    'TAI_SAN_CO_DINH':newValue,
                    'CONG_CU_DUNG_CU':newValue,
                    'THUE':newValue,
                    'KHO_BAN_HANG':newValue,
                    'GIA_THANH':newValue,
                    'KET_CHUYEN_LAI_LO_THEO_KY':newValue,
                    'BAO_CAO_TAI_CHINH':newValue,
                    'THU_QUY':newValue,
                    'THU_KHO':newValue,
                });
            }
        
        },
       
    });
    
    var KiemTraDoiChieuChungTuSoSachView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: KiemTraDoiChieuChungTuSoSachController,
        }),
    });
    
    view_registry.add('kiem_tra_doi_chieu_chung_tu_so_sach_form_view', KiemTraDoiChieuChungTuSoSachView);
    
    return KiemTraDoiChieuChungTuSoSachView;
});
