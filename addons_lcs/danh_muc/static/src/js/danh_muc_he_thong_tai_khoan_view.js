odoo.define('danh_muc.danh_muc_he_thong_tai_khoan_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var DanhMucHeThongTaiKhoanController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onFieldChanged: function(field){
            var self = this;
            var check = this.getFieldValue(field);
            if (field=='DOI_TUONG'){
               self.getFieldWidget('DOI_TUONG_SELECTION').do_active(check);
            }
            if (field=='DOI_TUONG_THCP'){
                self.getFieldWidget('DOI_TUONG_THCP_SELECTION').do_active(check);
            }
            if (field=='CONG_TRINH'){
                self.getFieldWidget('CONG_TRINH_SELECTION').do_active(check)
            }
            if (field=='DON_DAT_HANG'){
                self.getFieldWidget('DON_DAT_HANG_SELECTION').do_active(check)
            }
            if (field=='HOP_DONG_BAN'){
                self.getFieldWidget('HOP_DONG_BAN_SELECTION').do_active(check)
            }
            if (field=='HOP_DONG_MUA'){
                 self.getFieldWidget('HOP_DONG_MUA_SELECTION').do_active(check)
            }
            if (field=='KHOAN_MUC_CP'){
                 self.getFieldWidget('KHOAN_MUC_CP_SELECTION').do_active(check)
            }
            if (field=='DON_VI'){
                 self.getFieldWidget('DON_VI_SELECTION').do_active(check)
            }
            if (field=='MA_THONG_KE'){
                 self.getFieldWidget('MA_THONG_KE_SELECTION').do_active(check)
            }
        },
        
    });

    var DanhMucHeThongTaiKhoanRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var DanhMucHeThongTaiKhoanModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var DanhMucHeThongTaiKhoanView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: DanhMucHeThongTaiKhoanModel,
            Renderer: DanhMucHeThongTaiKhoanRenderer,
            Controller: DanhMucHeThongTaiKhoanController,
        }),
    });
    
    view_registry.add('danh_muc_he_thong_tai_khoan_view', DanhMucHeThongTaiKhoanView);
    
    return DanhMucHeThongTaiKhoanView;
});
