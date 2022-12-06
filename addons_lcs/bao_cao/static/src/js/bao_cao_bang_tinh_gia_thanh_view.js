odoo.define('bao_cao.bao_cao_bang_tinh_gia_thanh_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var BaoCaoBangTinhGiaThanhController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        onFieldChanged: function(field) {
            var self = this;
            
            if(field == 'PP_TINH_GIA_THANH'){
                var pp_tinh_gia_thanh = this.getFieldValue('PP_TINH_GIA_THANH');
                if (pp_tinh_gia_thanh=='PHUONG_PHAP_TINH_GIA_THANH_DON_GIAN'){
                    this.getFieldWidget('KY_TINH_GIA_THANH').changeDomain([['LOAI_GIA_THANH', '=', 'DON_GIAN']]);
                }
                else if(pp_tinh_gia_thanh=='PHUONG_PHAP_TINH_GIA_THANH_HE_SO_TY_LE'){
                    this.getFieldWidget('KY_TINH_GIA_THANH').changeDomain([['LOAI_GIA_THANH', '=', 'HE_SO_TY_LE']]);
                }

            }
        },
       
    });

   
    
    var BaoCaoBangTinhGiaThanhView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            
            Controller: BaoCaoBangTinhGiaThanhController,
        }),
    });
    
    view_registry.add('bao_cao_bang_tinh_gia_thanh_view', BaoCaoBangTinhGiaThanhView);
    
    return BaoCaoBangTinhGiaThanhView;
});
