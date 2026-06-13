import { createI18n } from 'vue-i18n'

const messages = {
  en: {
    sidebar: {
      dashboard: 'Dashboard',
      products: 'Products',
      users: 'Users',
      language: 'عربي'
    },
    dashboard: {
      title: 'Dashboard Overview',
      subtitle: 'Welcome back! Here\'s what\'s happening with your microservices today.',
      stats: {
        totalProducts: 'Total Products',
        activeUsers: 'Active Users',
        newOrders: 'New Orders',
        revenue: 'Revenue',
        thisMonth: 'this month'
      },
      recentActivities: 'Recent Activities',
      topProducts: 'Top Products'
    },
    products: {
      title: 'Products',
      subtitle: 'Manage your product inventory',
      addBtn: '+ Add Product',
      searchPlaceholder: 'Search products by name...',
      loading: 'Loading products...',
      empty: 'No products found. Add your first product!',
      columns: {
        id: 'ID',
        name: 'Name',
        category: 'Category',
        price: 'Price',
        stock: 'Stock',
        status: 'Status',
        actions: 'Actions'
      },
      status: {
        active: 'Active',
        inactive: 'Inactive'
      },
      modal: {
        title: 'Add New Product',
        save: 'Save Product',
        cancel: 'Cancel',
        nameLabel: 'Product Name',
        categoryLabel: 'Category',
        priceLabel: 'Price (USD)',
        stockLabel: 'Stock Quantity'
      },
      actions: {
        edit: 'Edit',
        delete: 'Delete'
      }
    },
    users: {
      title: 'Users',
      subtitle: 'Manage system access and accounts',
      inviteBtn: '+ Invite User',
      searchPlaceholder: 'Search users...',
      loading: 'Loading users...',
      status: {
        active: 'Active',
        inactive: 'Inactive'
      },
      roles: {
        admin: 'Admin',
        customer: 'Customer'
      },
      stats: {
        totalOrders: 'Total Orders: '
      },
      joined: 'Joined',
      edit: 'Edit'
    }
  },
  ar: {
    sidebar: {
      dashboard: 'لوحة القيادة',
      products: 'المنتجات',
      users: 'المستخدمين',
      language: 'English'
    },
    dashboard: {
      title: 'نظرة عامة على النظام',
      subtitle: 'مرحباً بعودتك! إليك ملخص لما يحدث في نظامك اليوم.',
      stats: {
        totalProducts: 'إجمالي المنتجات',
        activeUsers: 'المستخدمين النشطين',
        newOrders: 'الطلبات الجديدة',
        revenue: 'الأرباح',
        thisMonth: 'هذا الشهر'
      },
      recentActivities: 'النشاطات الأخيرة',
      topProducts: 'المنتجات الأكثر مبيعاً'
    },
    products: {
      title: 'المنتجات',
      subtitle: 'إدارة مخزون المنتجات',
      addBtn: '+ إضافة منتج',
      searchPlaceholder: 'ابحث عن منتج بالاسم...',
      loading: 'جاري تحميل المنتجات...',
      empty: 'لا توجد منتجات. أضف منتجك الأول!',
      columns: {
        id: 'الرقم',
        name: 'الاسم',
        category: 'التصنيف',
        price: 'السعر',
        stock: 'المخزون',
        status: 'الحالة',
        actions: 'الإجراءات'
      },
      status: {
        active: 'نشط',
        inactive: 'غير نشط'
      },
      modal: {
        title: 'إضافة منتج جديد',
        save: 'حفظ المنتج',
        cancel: 'إلغاء',
        nameLabel: 'اسم المنتج',
        categoryLabel: 'التصنيف',
        priceLabel: 'السعر (دولار)',
        stockLabel: 'كمية المخزون'
      },
      actions: {
        edit: 'تعديل',
        delete: 'حذف'
      }
    },
    users: {
      title: 'المستخدمين',
      subtitle: 'إدارة الصلاحيات وحسابات النظام',
      inviteBtn: '+ دعوة مستخدم',
      searchPlaceholder: 'ابحث عن مستخدمين...',
      loading: 'جاري تحميل المستخدمين...',
      status: {
        active: 'نشط',
        inactive: 'غير نشط'
      },
      roles: {
        admin: 'مدير',
        customer: 'عميل'
      },
      stats: {
        totalOrders: 'إجمالي الطلبات: '
      },
      joined: 'انضم في',
      edit: 'تعديل'
    }
  }
}

const i18n = createI18n({
  legacy: false, 
  locale: 'ar', 
  fallbackLocale: 'en',
  messages
})

export default i18n
