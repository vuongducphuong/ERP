odoo.define('danh_muc.danh_muc_loai_tien_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var DanhMucLoaiTienController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {               

                case "btn_lay_ngam_dinh_tieng_viet":
                    self.updateUI({'KY_HIEU_BAT_DAU': this.getFieldData('KY_HIEU_BAT_DAU_MAC_DINH'),
                    'DOC_TEN_LOAI_TIEN': this.getFieldData('DOC_TEN_LOAI_TIEN_MAC_DINH'),
                    'DOC_PHAN_CACH_THAP_PHAN': this.getFieldData('DOC_PHAN_CACH_THAP_PHAN_MAC_DINH'),
                    'DOC_SO_TIEN_SAU_THAP_PHAN': this.getFieldData('DOC_SO_TIEN_SAU_THAP_PHAN_MAC_DINH'),
                    'TY_LE_CHUYEN_DOI': this.getFieldData('TY_LE_CHUYEN_DOI_MAC_DINH'),
                    'KY_HIEU_KET_THUC': this.getFieldData('KY_HIEU_KET_THUC_MAC_DINH'),
                    });
                    break;
                    
                case "btn_lay_ngam_dinh_tieng_anh":
                    self.updateUI({'KY_HIEU_BAT_DAU_TIENG_ANH': this.getFieldData('KY_HIEU_BAT_DAU_TIENG_ANH_MAC_DINH'),
                    'DOC_TEN_LOAI_TIEN_TIENG_ANH': this.getFieldData('DOC_TEN_LOAI_TIEN_TIENG_ANH_MAC_DINH'),
                    'DOC_PHAN_CACH_THAP_PHAN_TIENG_ANH': this.getFieldData('DOC_PHAN_CACH_THAP_PHAN_TIENG_ANH_MAC_DINH'),
                    'DOC_SO_TIEN_SAU_THAP_PHAN_TIENG_ANH': this.getFieldData('DOC_SO_TIEN_SAU_THAP_PHAN_TIENG_ANH_MAC_DINH'),
                    'TY_LE_CHUYEN_DOI_TIENG_ANH': this.getFieldData('TY_LE_CHUYEN_DOI_TIENG_ANH_MAC_DINH'),
                    'KY_HIEU_KET_THUC_TIENG_ANH': this.getFieldData('KY_HIEU_KET_THUC_TIENG_ANH_MAC_DINH'),
                    });
                    break;
                
                default: 
                   this._super.apply(this, arguments);
            }
            
        },
        
    });

    var DanhMucLoaiTienRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var DanhMucLoaiTienModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var DanhMucLoaiTienView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: DanhMucLoaiTienModel,
            Renderer: DanhMucLoaiTienRenderer,
            Controller: DanhMucLoaiTienController,
        }),
    });
    
    view_registry.add('danh_muc_loai_tien_view', DanhMucLoaiTienView);
    
    return DanhMucLoaiTienView;
});
