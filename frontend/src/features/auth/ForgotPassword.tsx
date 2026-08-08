import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { Mail, ArrowLeft, CheckCircle2 } from 'lucide-react';
import api from '../../services/api';

type ForgotPasswordData = {
  email: string;
};

export const ForgotPassword: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<ForgotPasswordData>();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const onSubmit = async (data: ForgotPasswordData) => {
    setIsSubmitting(true);
    try {
      await api.post('/auth/forgot-password', data);
      setIsSuccess(true);
    } catch (err) {
      // We still show success to prevent email enumeration, as handled in the backend
      setIsSuccess(true);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isSuccess) {
    return (
      <div className="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-50 to-primary-50">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="glass-card text-center">
            <div className="flex justify-center text-green-500 mb-4">
              <CheckCircle2 size={48} />
            </div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Check your inbox</h2>
            <p className="text-slate-600 mb-6">
              If an account exists for that email, we have sent password reset instructions.
            </p>
            <Link to="/login" className="btn-primary w-full inline-block">
              Return to login
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col justify-center py-12 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-50 to-primary-50">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-slate-900">
          Reset your password
        </h2>
        <p className="mt-2 text-center text-sm text-slate-600">
          Enter your email and we'll send you a recovery link
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="glass-card">
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Email address</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-slate-400" />
                </div>
                <input
                  type="email"
                  {...register('email', { required: 'Email is required' })}
                  className="input-field pl-10"
                  placeholder="you@example.com"
                />
              </div>
              {errors.email && <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>}
            </div>

            <div>
              <button
                type="submit"
                disabled={isSubmitting}
                className="btn-primary disabled:opacity-70 flex items-center justify-center"
              >
                {isSubmitting ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
                ) : (
                  'Send recovery email'
                )}
              </button>
            </div>
            
            <div className="text-center mt-4">
              <Link to="/login" className="inline-flex items-center text-sm font-medium text-primary-600 hover:text-primary-500 transition-colors">
                <ArrowLeft size={16} className="mr-1" /> Back to login
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
