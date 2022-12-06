odoo.define('account_ex.account_ex_chi_phi_do_dang_cong_trinh_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

    var ChiPhiDoDangCongTrinhController = FormController.extend({
		
        onViewLoaded: function(e, defer) {
			var def = defer;
            var self = this;
            
            this.rpc_action({
                model: 'account.ex.chi.phi.do.dang.master',
                method: 'lay_du_lieu_cong_trinh',
                // args: {},
                callback: function(result) {
                    if (result) {
                        self.updateUI(result).then(function() {
                            var fieldWidget = self.getFieldWidget('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS');
                            var nhap_chi_tiet = self.getFieldValue('NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH');
                            if(nhap_chi_tiet == true){
                                fieldWidget.do_visible_columns(['MTC_CHI_PHI_NVL_GIAN_TIEP','MTC_CHI_PHI_NHAN_CONG','MTC_CHI_PHI_KHAU_HAO_DAU_KY','MTC_CHI_PHI_MUA_NGOAI_DAU_KY','MTC_CHI_PHI_KHAC_CHUNG','CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','CHI_PHI_KHAU_HAO','CHI_PHI_MUA_NGOAI','TONG_CHI_PHI','Máy thi công','Chi phí chung'], true);
                                fieldWidget.do_visible_columns(['MAY_THI_CONG'], false);
                            }else{
                                fieldWidget.do_visible_columns(['MTC_CHI_PHI_NVL_GIAN_TIEP','MTC_CHI_PHI_NHAN_CONG','MTC_CHI_PHI_KHAU_HAO_DAU_KY','MTC_CHI_PHI_MUA_NGOAI_DAU_KY','MTC_CHI_PHI_KHAC_CHUNG','CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','CHI_PHI_KHAU_HAO','CHI_PHI_MUA_NGOAI','TONG_CHI_PHI','Máy thi công','Chi phí chung'], false);
                                fieldWidget.do_visible_columns(['MAY_THI_CONG'], true);
                            }
                        	if (def) {
								def.resolve();
							}
                        });
                    }
					
                }
            });
        },
        onFieldChanged: function(field){
            var self = this;
            if("NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH" == field){
            		
					Dialog.show_message('', 'Nếu tích chọn Nhập chi tiết theo các yếu tố chi phí thì số liệu bạn nhập trên khoản mục Chi phí chung sẽ hiển thị trên yếu tố Chi phí khác. Bạn có muốn tiếp tục thực hiện không?', 'CONFIRM')
					.then(function(result) {
                        var fieldWidget = self.getFieldWidget('ACCOUNT_EX_CHI_PHI_DO_DANG_IDS');
						if(result == true){
                            if(self.getFieldValue('NHAP_CHI_TIET_LOAI_CPDD_CONG_TRINH') == true){
                                fieldWidget.do_visible_columns(['MTC_CHI_PHI_NVL_GIAN_TIEP','MTC_CHI_PHI_NHAN_CONG','MTC_CHI_PHI_KHAU_HAO_DAU_KY','MTC_CHI_PHI_MUA_NGOAI_DAU_KY','MTC_CHI_PHI_KHAC_CHUNG','CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','CHI_PHI_KHAU_HAO','CHI_PHI_MUA_NGOAI','TONG_CHI_PHI','Máy thi công','Chi phí chung'], true);
                                fieldWidget.do_visible_columns(['MAY_THI_CONG'], false);
                            }
                            else{
                                fieldWidget.do_visible_columns(['MTC_CHI_PHI_NVL_GIAN_TIEP','MTC_CHI_PHI_NHAN_CONG','MTC_CHI_PHI_KHAU_HAO_DAU_KY','MTC_CHI_PHI_MUA_NGOAI_DAU_KY','MTC_CHI_PHI_KHAC_CHUNG','CHI_PHI_NVL_GIAN_TIEP','CHI_PHI_NHAN_CONG_GIAN_TIEP','CHI_PHI_KHAU_HAO','CHI_PHI_MUA_NGOAI','TONG_CHI_PHI','Máy thi công','Chi phí chung'], false);
                                fieldWidget.do_visible_columns(['MAY_THI_CONG'], true);
                            }
                        }
				});
                
            }
        }
    });
    
    var ChiPhiDoDangCongTrinhView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: ChiPhiDoDangCongTrinhController,
        }),
    });
    
    view_registry.add('account_ex_chi_phi_do_dang_cong_trinh_form_view', ChiPhiDoDangCongTrinhView);
    
    return ChiPhiDoDangCongTrinhView;
});