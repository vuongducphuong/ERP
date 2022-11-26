odoo.define('gia_thanh.chon_ky_tinh_gia_thanh_ket_chuyen_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var ChonKyTinhGiaThanhKetChuyenFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        onViewLoaded: function(e, defer) {
            var self = this;
			var def =  defer;
			if (self.params && self.params.tham_so){
					this.getFieldWidget('KY_TINH_GIA_THANH_ID').changeDomain([['LOAI_GIA_THANH','=',self.params.tham_so]]);
			}

            def.resolve();
        },
    });
    
    var ChonKyTinhGiaThanhKetChuyenFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
           
            Controller: ChonKyTinhGiaThanhKetChuyenFormController,
        }),
    });
    
    view_registry.add('chon_ky_tinh_gia_thanh_ket_chuyen_form_view', ChonKyTinhGiaThanhKetChuyenFormView);
    
    return ChonKyTinhGiaThanhKetChuyenFormView;
});
